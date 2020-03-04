$(function () {
    $('#btnCont').on('click', function () {
        $('#dataInitial').removeClass('hidden');
        //crear dinamicamente los campos
        let amountVariables = $('#amountVariables').val();
        let amountRestrictions = $('#amountRestrictions').val();
        generateInputs(amountVariables, amountRestrictions)
    });

    function generateInputs(amountVariables, amountRestrictions) {
        let html = '';
        let select = ' <select class="" style="width: 45px !important;">\n' +
            '                <option selected>≤</option>\n' +
            '                <option>≥</option>\n' +
            '                <option>=</option>\n' +
            '            </select>';
        let innput = '<input type="text" class="form-control" placeholder=""\n' +
            '                   aria-label=""\n' +
            '                   aria-describedby="basic-addon2">';
        for (let i = 0; i < amountRestrictions; i++) {
            html += '<div class="input-group mb-3">';
            for (let j = 0; j < amountVariables; j++) {
                html += innput  +  ' + <span>X<sub>' + (j + 1) + '</sub></span> + ';
            }
            html += select + innput;
            html += '</div>';
        }
        html += ' <div class="input-group-append">\n' +
            '            <button class="btn  btn-success m-auto" type="button">Continuar</button>\n' +
            '        </div>';
        $('#dataInitial').append(html);
    }
}());


