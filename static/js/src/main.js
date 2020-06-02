/**
 * Script principal
 *
 * @author Luis Guillermo Gómez Galeano <luis.gomez@usantoto.edu.co>
 * @author Oscar Javier Gómez Sánchez <oscar.gomezs@usantoto.edu.co>
 *
 * @version 1.0
 *
 */

$(document).ready(function () {

    /**
     * Generar campos
     */
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

    /**
     * Genera un campo de texto
     * @param id ID del campo de texto
     * @returns {string} HTML del campo de texto
     */
    function generateInputText(id) {
        return `<input type="text" class="form-control form-control-sm" name="restriction-${id}" id="restriction-${id}">`;
    }

    /**
     * Genera una etiqueta select
     * @param id ID de la etiqueta select
     * @returns {string} HTML de la etiqueta select
     */
    function generateInputSelect(id) {
        return `<select id="restriction-sign-${id}" name="restriction-sign-${id}" class="mr-2" style="width: 45px !important;">
                <option value="1" selected="">≤</option><option value="2">≥</option><option value="3">=</option></select>`;
    }

    // Validar formulario y generar campos para ingresar los datos del modelo
    $("#simplex_data").validate({
        errorClass: "text-danger label-validate",
        submitHandler: (form, event) => {
            event.preventDefault();
            generateInputs();
            $("#data-container").removeClass('d-none');
            validateData();
        },
        rules: {
            amount_variables: {
                required: true,
                maxlength: 5,
                number: true
            },
            amount_restrictions: {
                required: true,
                number: true,
                maxlength: 5
            }
        },
        messages: {
            amount_variables: {
                required: "Este campo es obligatorio",
                number: "Ingresa un número valido",
                maxlength: "Los caracteres ingresados son demasiados!"
            },
            amount_restrictions: {
                required: "Este campo es obligatorio",
                number: "Ingresa un número valido",
                maxlength: "Los caracteres ingresados son demasiados!"
            }
        }
    });

    // Validar formulario cuando ingresa los datos del modelo
    $("#data-container").validate({
        highlight: function (element) {
            $(element).addClass("border-danger");
        },
        unhighlight: function (element) {
            $(element).removeClass("border-danger");
        },
        submitHandler: (form, event) => {
            event.preventDefault()
            sendData()
        }
    });

    /**
     *  Validar los campos de texto cuando el usuario ingresa el modelo
     */
    function validateData() {
        $('[name^="coefficient"], [name^="restriction"]').each(function () {
            $(this).rules('add', {
                required: true,
                number: true,
                maxlength: 5,
                messages: {
                    required: "",
                    number: "",
                    maxlength: ""
                }
            })
        });
    }

    /**
     * Enviar datos al servidor para solucionar el modelo
     */
    function sendData() {
        let col_values = []
        let z_equation = []
        $("input[name^='restriction']").each(function () {
            col_values.push(parseInt($(this).val()))
        });
        $("input[name^='coefficient']").each(function () {
            z_equation.push(parseInt($(this).val()))
        });

        $.ajax({
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                quantity_variables: $('#amount_variables').val(),
                quantity_constrains: $('#amount_restrictions').val(),
                col_values: col_values,
                z_equation: z_equation
            })
        }).done(function (res) {
            showResults(res);
        }).fail(function (error) {
            console.log("error:", error);
        })
    }

    /**
     * Limpia la interfaz gráfica para realizar otro ejercicio
     */
    $('#btn_new').on('click', function () {
        $(this).removeClass('d-block').addClass('d-none');
        $('#data-container').addClass('d-none');
        $('#results, #restriction-div, #coefficient-div').empty();
    });

    /**
     * Mostrar resultados
     * @param data Datos en formato JSON
     */
    function showResults(data) {
        let html = ``;
        $.each(data.data, function (index, obj) {
            html += `<div class="table-responsive">
                        <table class="table table-bordered table-hover">
                        <thead><tr><th scope="col">Base</th>`;
            $.each(obj.columns, function (index, value) {
                html += `<th scope="col">${value}</th>`;
            });
            html += `</tr></thead><tbody>`;
            $.each(obj.data, function (index, value) {
                html += `<tr> <th scope="row">${obj.index[index]}</th>`;
                $.each(value, function (index, value) {
                    html += `<td>${value}</td>`;
                });
                html += `</tr>`;
            });
            html += `</tbody></table></div>`;

            if (obj.pivot_column && obj.pivot_row) {
                html += `<div class="card card-body mb-5">
                        <p class="card-text">Pivote: <span class="badge badge-custom-primary badge-pill">${obj.pivot_element}</span></p>
                        <p class="card-text">Fila pivote: <span class="badge badge-custom-primary badge-pill">`;
                for (let i = 0; i < obj.pivot_row.length; i++) {
                    html += `${obj.pivot_row[i]} ${i !== (obj.pivot_row.length - 1) ? ',' : ''} `;
                }
                html += `</span></p>
                    <p class="card-text">Columna pivote: <span class="badge badge-custom-primary badge-pill">`;
                for (let i = 0; i < obj.pivot_column.length; i++) {
                    html += `${obj.pivot_column[i]} ${i !== (obj.pivot_column.length - 1) ? ',' : ''} `;
                }
                html += `</span></p></div>`;
            }
            if (index === (data.data.length - 1)) {
                html += `<hr><div class="card card-body mt-4 mb-5">
                <h4 class="card-title">Solución óptima</h4>`;

                $.each(obj.data, function (index, value) {
                    html += `<p class="card-text font-weight-bold">${obj.index[index]} = ${value[value.length - 1]}</p>`;
                });

                html += `</div>`;
            }
        });
        $('#results').html(html);
        $('#btn_new').removeClass('d-none').addClass('d-block');
    }

});