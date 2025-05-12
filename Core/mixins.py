from django.db import models
from rest_framework import serializers

from .fields import SerializerImageField


class RepMixin(object):

    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping.update({models.ImageField: SerializerImageField})
        self.display_fields = kwargs.pop('display_fields', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        if self.display_fields is not None:
            allowed = set(self.display_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        ret = super().to_representation(instance)
        ret['__str__'] = str(instance)

        # Iterate over all fields of the instance
        for field_name, field in self.fields.items():

            if hasattr(field, 'choice_strings_to_values') and field.choice_strings_to_values:
                raw_value = ret[field_name]  # Get the raw value from the initially processed representation
                display_value = getattr(instance, f'get_{field_name}_display')()
                ret[field_name] = {
                    'id': raw_value,
                    'name': display_value
                } if display_value else None

            if isinstance(field, serializers.DateField):
                value = getattr(instance, field_name,None)
                if value:
                    formatted_date = value.strftime('%d/%m/%Y')
                    ret[field_name] = formatted_date

            if isinstance(field, serializers.DateTimeField):
                value = getattr(instance, field_name,None)
                if value:
                    formatted_date = value.strftime('%d/%m/%Y %H:%M:%S')
                    ret[field_name] = formatted_date

            if isinstance(field, serializers.FileField):
                value = getattr(instance, field_name,None)
                def readable_size(size_in_bytes):
                    if size_in_bytes < 1024:
                        return f"{size_in_bytes} Bytes"
                    size_in_kb = size_in_bytes / 1024
                    if size_in_kb < 1024:
                        return f"{size_in_kb:.2f} KB"
                    size_in_mb = size_in_kb / 1024
                    return f"{size_in_mb:.2f} MB"

                def get_file_name_from_url(url):
                    # Split the URL by '/' and return the last part
                    return url.split('/')[-1]

                if value:
                    request = self.context.get('request')
                    detailed_value = {
                        'url': request.build_absolute_uri(value.url) if request else value.url,
                        'size': readable_size(value.size),
                        'name': get_file_name_from_url(value.name)
                    }
                    field_name = f"{field_name}_data"
                    ret[field_name] = detailed_value

        return ret
