$(function(){
    $(document).ready(function(){
        addListener();
        checkEmpty();
    });
});

function checkEmpty() {
    var locavel = $('#id_locavel').val();
    var data_id = $('#id_atividade').attr('data-select-id');
    if (!locavel) {
        $('#id_atividade').html('<option value="">---------</option>');
    } else {
        var atividade = $('#id_atividade').val();
        sendData(locavel, atividade);
    }
}

function setStarting(atividade) {
    $('#id_atividade option').each(function() {
        if ($(this).val() === atividade) {
            $(this).attr('selected', 'selected');
        }
    });
}

function sendData(locavel, atividade){
    var csrftoken = getCookie('csrftoken');
    var title = $('#content').children('h1').text();
    $.ajax({
        type: 'POST',
        url: '/get_atividade_set/',
        data: {
            locavel: locavel,
            title: title,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
        success: function(data) {
            updateOptions(data);
            if (!!atividade) setStarting(atividade);
        }
    });
}

function updateOptions(data) {
    var options = '<option value="">---------</option>';
    for (i = 0; i < data.atividades.length; i++) {
        options += '<option value="'+data.ids[i]+'">'+data.atividades[i]+'</option>';
    }
    $('#id_atividade').html(options);
    addListener();
}

function addListener() {
    $('#id_locavel option').on('click', function() {
        var id = $(this).attr('value');
        if (id) {
            sendData(id, null);
        } else {
            var options = '<option value="">---------</option>';
            $('#id_atividade').html(options);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}