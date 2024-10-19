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
                $('#transaction-category').append('<option value="">Select Category</option>'); // Changed from "Select Staff"

                $.each(response.categories, function(index, category) {
                    $('#transaction-category').append('<option value="'+category.slug+'">'+category.name+'</option>');
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching categories:', error);
            }
        });
    });
});
