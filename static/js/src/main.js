$(document).ready(function () {
    function generateInputs() {
        let amount_variables = $('#amount_variables').val()
        let amount_restrictions = $('#amount_restrictions').val()
        let html = ``;
        let non_negative_variables = ``;

        for (let i = 0; i < amount_variables; i++) {
            html += `<input type="text" class="form-control form-control-sm" name="coefficient-${i}" id="coefficient-${i}">
                <label for="coefficient-${i}" class="mx-1">X<sub>${i + 1}</sub>${i !== (amount_variables - 1) ? '+' : ''}</label>`;
            non_negative_variables += `X<sub>${i + 1}</sub>${i !== (amount_variables - 1) ? ', ' : ''}`;
        }
        non_negative_variables += ` ≥ 0`;
        $('#coefficient-div').html(html);
        $('#non-negative-variables').html(non_negative_variables);
        html = ``;

        for (let i = 0; i < amount_restrictions; i++) {
            html += '<div class="input-group mb-3">';
            for (let j = 0; j < amount_variables; j++) {
                if ((j + 1) === amount_variables) {
                    html += generateInputText(i + "" + j) + `<label for="restriction-${i}${j}" class="mx-1">X<sub>${j + 1}</sub></label>`;
                } else {
                    html += generateInputText(i + "" + j) + `<label for="restriction-${i}${j}" class="mx-1">X<sub>${j + 1}</sub> +</label>`;
                }
            }
            html += generateInputSelect(i) + generateInputText(i) + '</div>';
        }
        $('#restriction-div').html(html);
    }

    function generateInputText(id) {
        return `<input type="text" class="form-control form-control-sm" name="restriction-${id}" id="restriction-${id}">`;
    }

    function generateInputSelect(id) {
        return `<select id="restriction-sign-${id}" name="restriction-sign-${id}" class="mr-2" style="width: 45px !important;">
                <option value="1" selected="">≤</option><option value="2">≥</option><option value="3">=</option></select>`;
    }

    $('#next-1').on('click', function () {
        generateInputs()
    })


    $('#btn_send').on('click', function () {
        let col_values = []
        let cantidad_variables = 2;
        let cantidad_constrains = 3;
        let ecuacion_Z = []
        $("input[name^='restriction']").each(function () {
            col_values.push(parseInt($(this).val()))
        });
        $("input[name^='coefficient']").each(function () {
            console.log($(this).val());
            ecuacion_Z.push(parseInt($(this).val()))
        });
        console.log("ARRAY", ecuacion_Z)

        $.ajax({
            method: 'POST',
            dataType: 'json',
            "content-type": 'application/json',
            data: JSON.stringify({
                cantidad_variables: $('#amount_variables').val(),
                cantidad_constrains: $('#amount_restrictions').val(),
                col_values: col_values,
                ecuacion_Z: ecuacion_Z
            })
        }).done(function (res) {
            console.log(111111111111)
            window.location.href = res.url;
        }).fail(function (error) {
            console.log("error:", error);
        })
    })
});