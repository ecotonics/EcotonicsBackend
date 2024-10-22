$(document).ready(function() {
    $('#transaction-type').on('change', function() {
        var type = $(this).val();

        $.ajax({
            url: '/accounts/filter-category/',
            data: {
                'type': type
            },
            success: function(response) {
                $('#transaction-category').empty();
                $('#transaction-category').append('<option value="">Select Category</option>');

                $.each(response.categories, function(index, category) {
                    $('#transaction-category').append('<option value="'+category.slug+'">'+category.name+'</option>');
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching categories:', error);
            }
        });
    });

    $('#service-category').on('change', function() {
        var slug = $(this).val();

        $.ajax({
            url: '/filter-service/',
            data: {
                'slug': slug
            },
            success: function(response) {
                $('#services').empty();
                $('#services').append('<option value="">Select Service</option>');

                $.each(response.services, function(index, service) {
                    $('#services').append('<option value="'+service.slug+'">'+service.name+'</option>');
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching categories:', error);
            }
        });
    });
});
