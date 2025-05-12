from datetime import date, datetime
from io import BytesIO

import cairosvg
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.forms.fields import ImageField
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import FileField


def convert_svg_to_png(svg_data):
    png_data = cairosvg.svg2png(bytestring=svg_data)
    output_file_name = 'converted_images/output_file.png'
    path = default_storage.save(output_file_name, ContentFile(png_data))
    return path


class SvgImageField(ImageField):
    def to_python(self, data):
        if data is None:
            return None

        if hasattr(data, "temporary_file_path"):
            file_path = data.temporary_file_path()
            with open(file_path, 'rb') as file:  # Open in binary mode
                content = file.read(1024)  # Read the first 1024 bytes
        else:
            if hasattr(data, "read"):
                content = data.read(1024)  # Read first 1024 bytes
                data.seek(0)  # Reset pointer to the start of the file
                file = BytesIO(data.read())  # Re-read the whole file if necessary
            else:
                content = data["content"][:1024]
                file = BytesIO(data["content"])

        is_svg = b'<svg' in content.lower()

        if is_svg:
            # Reset data position for complete read if necessary
            if hasattr(data, "seek") and callable(data.seek):
                data.seek(0)
            svg_data = data.read() if hasattr(data, "read") else data["content"]
            # Convert SVG and get path to saved PNG
            saved_path = convert_svg_to_png(svg_data)
            # Reassign 'file' with the PNG data for further processing
            data = default_storage.open(saved_path)
            data.name = data.name.split('/')[-1]
            content = data.read(1024)
            data.seek(0)

        # Use ImageField's to_python method to further process the file
        f = super(ImageField, self).to_python(data)
        if f is None:
            return None

        from PIL import Image
        try:
            # Load and verify the image using PIL
            if is_svg:
                image = Image.open(data)  # For SVG converted to PNG
            else:
                image = Image.open(file)
            image.verify()

            # Annotate so subclasses can reuse for their own validation
            f.image = image
            f.content_type = Image.MIME.get(image.format)

        except Exception as exc:
            # Raise a validation error if it's not a valid image
            raise ValidationError(
                self.error_messages["invalid_image"],
                code="invalid_image",
            ) from exc

        if hasattr(f, "seek") and callable(f.seek):
            f.seek(0)
        return f

class SerializerImageField(FileField):

    default_error_messages = {
        'invalid_image': _(
            'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'
        ),
    }

    def __init__(self, **kwargs):
        self._DjangoImageField = kwargs.pop('_DjangoImageField', SvgImageField)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        file_object = super().to_internal_value(data)
        django_field = self._DjangoImageField()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)
