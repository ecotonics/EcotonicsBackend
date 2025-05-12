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

    $('#customer_type').on('change', function(){
        var customer_type = $(this).val();

        $.ajax({
            url: '/filter-customers/',
            data: {
                'type': customer_type
            },
            success: function(response) {
                $('#customers').empty();
                $('#customers').append('<option value="">Select Customer</option>');

                $.each(response.customers, function(index, customer) {
                    $('#customers').append('<option value="'+customer.slug+'">'+customer.name+'</option>');
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching customers:', error);
            }
        });
    })

    $('#lead_type').on('change', function(){
        var lead_type = $(this).val();
        if (lead_type == 'new') {
            $('.new').show();
            $('.existing').hide();
        } else {
            $('.existing').show();
            $('.new').hide();
        }
    })
});
