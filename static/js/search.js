$(document).ready(function() {
    $('#search-input').on('input', function() {
        let query = $(this).val();
        let field = $('#search-field').val();

        if (query.length >= 3) {
            $.ajax({
                url: '/search',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ query: query, field: field }),
                success: function(data) {
                    let tableBody = $('tbody');
                    tableBody.empty();
                    data.forEach(function(avisation) {
                        tableBody.append(`
                            <tr>
                                <td>${avisation.id}</td>
                                <td>${avisation.car_number}</td>
                                <td>${avisation.driver_name}</td>
                                <td>${avisation.company_name}</td>
                                <td>${avisation.entry_time}</td>
                                <td>${avisation.exit_time}</td>
                                <td>${avisation.type}</td>
                                <td>${avisation.status}</td>
                                <td>
                                    <a href="/${avisation.id}/edit" class="btn btn-sm btn-warning">Редагувати</a>
                                    <form action="/${avisation.id}/delete" method="post" style="display: inline-block;">
                                        <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Ви впевнені?')">Видалити</button>
                                    </form>
                                </td>
                            </tr>
                        `);
                    });
                }
            });
        }
    });
});
