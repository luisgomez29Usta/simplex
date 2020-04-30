$(document).ready(function () {
    $('#send').on('click', function () {
        // alert('Sending')

        $.ajax({
            method: 'POST',
            dataType: 'json',
            "content-type": 'application/json',
            headers: {
                "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val(),
            },
            data: JSON.stringify({
                cantidad_variables: 2,
                cantidad_constrains: 3,
                col_values: [1.0, 0.0, 4.0,
                    0.0, 2.0, 12.0,
                    3.0, 2.0, 18.0],
                ecuacion_Z: [-3, -5]
            })
        }).done(function (res) {
            console.log(111111111111)
            window.location.href = res.url;
        }).fail(function (error) {
            console.log("error:", error);
        })
    })
});