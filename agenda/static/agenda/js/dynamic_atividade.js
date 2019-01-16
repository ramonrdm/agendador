$(function(){
    checkEmpty();
    update();
});

function checkEmpty() {
    var locavel = $('#id_locavel').parent().children('.select-dropdown').attr('value');
    var data_id = $('#id_atividade').attr('data-select-id');
    if (locavel === '---------') {
        $('#id_atividade').html('<option value="">---------</option>');
        $('#select-options-'+data_id).html('<li class=""><span>---------</span></li>');
    } else {
        var atividade = $('#id_atividade').parent().children('.select-dropdown').attr('value');
        sendData(locavel, atividade);
    }
}

function setStarting(atividade) {
    $('#id_atividade').parent().children('.select-dropdown').attr('value', atividade);
    $('#id_atividade option').each(function() {
        if ($(this).text() === atividade) {
            $(this).attr('selected', 'selected');
        }
    });
}

function update() {
    setTimeout( function() {
        var data_id = $('#id_locavel').attr('data-select-id');
        $('#select-options-'+data_id+' li').on('click', function() {
            sendData($(this).text(), null);
            update();
        });
    }, 10);
}

function sendData(locavel, atividade){
    var csrftoken = getCookie('csrftoken');
    var title = $('.page-title').text();
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
    var data_id = $('#id_atividade').attr('data-select-id');
    var options = '<option value="">---------</option>';
    var lelements = '<li class=""><span>---------</span></li>';
    for (i = 0; i < data.atividades.length; i++) {
        options += '<option value="'+data.ids[i]+'">'+data.atividades[i]+'</option>';
        lelements += '<li class=""><span>'+data.atividades[i]+'</span></li>';
    }
    $('#id_atividade').html(options);
    $('#select-options-'+data_id).html(lelements);
    $('#select-options-'+data_id).parent().children('.select-dropdown').attr('value', '---------');
    addListener(data_id);
}

function addListener(data_id) {
    $('#select-options-'+data_id+' li').on('click', function() {
        var text = $(this).text();
        $(this).parent().parent().children('.select-dropdown').attr('value', text);
        $($(this).parent().parent().find('option')).each(function() {
            if ($(this).text() === text) {
                $(this).attr('selected', 'selected');
            } else {
                $(this).removeAttr('selected');
            }
        });
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