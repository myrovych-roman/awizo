$(document).ready(function() {
    $('.status-select').on('change', function() {
        let status = $(this).val();
        let id = $(this).data('id');

        $.ajax({
            url: '/' + id + '/status',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ status: status }),
            success: function(data) {
                if (data.success) {
                    // Optionally show a success message
                }
            }
        });
    });
});
