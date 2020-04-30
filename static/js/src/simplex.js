$(function () {
    let amountVariables = 0;
    let amountRestrictions = 0;
    $('#nextBtn1').on('click', function () {
        $('#dataInitial').removeClass('hidden');
        //crear dinamicamente los campos
        amountVariables = $('#amountVariables').val();
        amountRestrictions = $('#amountRestrictions').val();
        generateInputs()
    });

    function generateInputs() {
        let html = '';
        let counter = 0;
        html += '<p>Ingrese los coeficientes de la función objetivo</p>';
        html += '<div class="input-group mb-3"><input type="text" id="inputtextxx" name="inputtext-00" class="form-control"><span>X<sub>1</sub></span> + <input type="text" id="inputtextxx1" name="inputtext-01" class="form-control"><span>X<sub>2</sub></span><select id="inputselectx2" class="" style="width: 45px !important;">\n' +
            '                            <option value="1" selected="">≤</option>\n' +
            '                            <option value="2">≥</option>\n' +
            '                            <option value="3">=</option>\n' +
            '                         </select><input type="text" id="inputtextxx2" name="inputtext-02" class="form-control"></div>';
        html += '<p>Ingrese las funciones restricción</p>';
        for (let i = 0; i < amountRestrictions; i++) {
            html += '<div class="input-group mb-3">';
            for (let j = 0; j < amountVariables; j++) {
                if ((j + 1) == amountVariables) {
                    html += generateInputText(i + "" + j) + '<span>X<sub>' + (j + 1) + '</sub></span>';
                } else {
                    html += generateInputText(i + "" + j) + '<span>X<sub>' + (j + 1) + '</sub></span> + ';
                }
                counter = j + 1;
            }
            html += genereteInputSelect(i + counter) + generateInputText(i + "" + counter) + '</div>';
            counter++;
        }
        html += `<div class="input-group-append">
                    <button id="nextBtn2" class="btn  btn-success m-auto" type="button">Continuar</button>\\n' +
                </div>`;
        $('#dataInitial').append(html);
        $('#nextBtn2').on('click', function () {
            getDataInputs();
        });
    }

    function generateInputText(id) {
        return `<input type="text" id="inputtext${id}" name="inputtext-${id}" class="form-control">`
    }

    function genereteInputSelect(id) {
        return select = `<select id="inputselect${id}" class="" style="width: 45px !important;">
                            <option value="1" selected>≤</option>
                            <option value="2">≥</option>
                            <option value="3">=</option>
                         </select>`;
    }

    function getDataInputs() {
        let variables = [];
        let params = $('[id^=inputtext]');
        let html = "";
        let contador = 0;
        for (let i = 0; i < params.length; i++) {
            console.log(params[i].value)
        }
        for (let i = 0; i < amountRestrictions; i++) {
            html += '<p>';
            for (let j = 0; j < amountVariables; j++) {
                html += `${params[contador].value}<span>X<sub>${j + 1}</sub></span> + `;
                console.log('contador',contador);
                contador++;
                if((j+1) == amountVariables){
                    html += ` = ${params[contador].value}<span>X<sub>${j + 1}</sub></span> `;

                }
            }
            html += '</p>';
        }
        let container = $('#doingData');
        container.append(html);
        container.removeClass('hidden');
    }
}());


