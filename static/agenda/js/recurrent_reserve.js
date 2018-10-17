var hidden = true;

$(function()
{
    $(document).ready(function() {
        prevent_default_submit();
        initialize_date_inputs();
        var question_mark = create_and_return_questionmark();
        add_tooltip(question_mark);
        add_listeners_to_option();
        create_confirmation_modal();
    });
});

function prevent_default_submit() {
    var submit_button = $(".right-align").find('button:first');
    submit_button.on("click", function( event ) {
        if (!hidden)
        {
            event.preventDefault();
            update_modal_dates();
            $("#recurrent-modal").modal('open');
        }
    });
}

function initialize_date_inputs()
{
    if ($("#id_recorrente").attr('checked')) {
        show_inputs();
        hidden = false;
    }
}

function add_listeners_to_option()
{
    $('#id_recorrente').on("click", function() {
        if (hidden)
        {
            show_inputs();
        }
        else
        {  
            hide_date_inputs();
        }
    });
}

function show_inputs()
{
    $('#id_dataInicio_container').css('display', 'initial');
    $('#id_dataFim_container').css('display', 'initial');
    $('#id_seg_container').css('display', 'initial');
    $('#id_ter_container').css('display', 'initial');
    $('#id_qua_container').css('display', 'initial');
    $('#id_qui_container').css('display', 'initial');
    $('#id_sex_container').css('display', 'initial');
    $('#id_sab_container').css('display', 'initial');
    $('#id_dom_container').css('display', 'initial');
    hidden = false;
}

function hide_date_inputs()
{
    $('#id_dataInicio_container').css('display', 'none');
    $('#id_dataFim_container').css('display', 'none');
    $('#id_seg_container').css('display', 'none');
    $('#id_ter_container').css('display', 'none');
    $('#id_qua_container').css('display', 'none');
    $('#id_qui_container').css('display', 'none');
    $('#id_sex_container').css('display', 'none');
    $('#id_sab_container').css('display', 'none');
    $('#id_dom_container').css('display', 'none');
    hidden = true;
}

function add_tooltip(question_mark)
{
    var tooltip_text = `
        Reserva recorrente cria reservas em todos os dias da semana<br>
        iguais à data selecionada entre certo período.<br>
        <br>
        Ex: Todas as segundas, terças e quartas, das 10:00 às 11:00, de 23/01/18 até 23/06/18.
    `;
    question_mark.attr('data-tooltip', tooltip_text);
    question_mark.tooltip({delay: 50, html: true});
    question_mark.on("click", function(event) {
        event.preventDefault();
    });
    question_mark.css("cursor", "default");
}

function create_and_return_questionmark()
{
    var label = $('#id_recorrente_container').find('label:first');
    var question_mark = '    <i class="tiny material-icons question_mark tooltipped">help_outline</i>';
    var new_label = label + question_mark;
    $(label).append(question_mark);
    var question_mark = $(document).find('.question_mark');
    question_mark.css('color', '#039be5');
    return question_mark;
}

function update_modal_dates()
{
    var starting_date = '';
    if ($('#id_dataInicio').attr('type') !== 'hidden')
    {
        starting_date = $('#id_dataInicio').val();
    }
    else
    {
        starting_date = $('#id_data').val();
    }
    var ending_date = $('#id_dataFim').val();

    $("#starting_date").text(starting_date);
    $("#ending_date").text(ending_date);
}

function create_confirmation_modal()
{

    var ending_date = $('#id_dataFim').val();
    var modal_html = `
        <div id="recurrent-modal" class="modal">
            <div class="modal-content">
                <h4>Reserva Recorrente</h4>
                <p>Essa é uma reserva recorrente, alterações aqui feitas terão efeito nas reservas recorrentes do dia <span id="starting_date"></span> ao dia <span id="ending_date"></span>.<p>
                Caso deseje editar apenas essa reserva, certifique-se de que a opção "Recorrente" está desmarcada.
            </div>
            <div class="modal-footer">
                <a id="submit_button" type="submit" class="modal-action modal-close waves-effect waves-green btn-flat">Concordar</a>
                <a id="close-modal" class="modal-action modal-close waves-effect waves-green btn-flat">Retornar</a>
            </div>
        </div>
    `
    $('form').append(modal_html);
    $('#recurrent-modal').modal({endingTop: '30%'});
    $("#submit_button").on("click", function() {
        try_submit_form();
    });
}

function try_submit_form()
{
    var status = $('#id_estado').val();
    if (status == 'A') {
        var checked_week_days = get_selected_days();
        var ending_date = $('#id_dataFim').val();
        var reservable_type = $('.page-title').text();
        var reservable_name = $('#id_locavel').parent().children('.select-dropdown').attr('value');
        var date = $('#id_data').val();
        var starting_time = $('#id_horaInicio').val();
        var ending_time = $('#id_horaFim').val();
        check_other_reserves(reservable_type, reservable_name, date, starting_time, ending_time, ending_date, checked_week_days);
    } else {
        $('form').submit();
    }
}

function check_other_reserves(reservable_type, reservable_name, date, starting_time, ending_time, ending_date, checked_week_days)
{    
    var csrftoken = getCookie('csrftoken');
    var current_url = window.location.href;
    var current_url = current_url.split("/");
    var current_reserve_id = parseInt(current_url[current_url.length-3])
    $.ajax({
        async: false,
        type: 'POST',
        url: '/get_pending_reserves/',
        data: {
            reservable_type: reservable_type,
            reservable_name: reservable_name,
            date: date,
            ending_date: ending_date,
            starting_time: starting_time,
            ending_time: ending_time,
            checked_week_days: checked_week_days,
            current_reserve_id: current_reserve_id,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
        success: function(data) {
            check_server_response(data);
        }
    });
}

function check_server_response(server_response) {
    if (server_response.conflict_reserves) {
        $("#recurrent-modal").modal('close');
        update_confirmation_modal(server_response.conflict_reserves_names, server_response.conflict_reserves_ids);
        $("#confirmation-modal").modal('open');
    } else {
        $("form").submit();
    }
}

function update_confirmation_modal(reserves_names, reserves_ids) {
    $('#other_reserves_list').html('');
    var current_url = window.location.href;
    current_url = current_url.split('/');
    var html = '';
    for (var i = 0; i < reserves_ids.length; i++) {
        current_url[current_url.length-3] = reserves_ids[i];
        var url = current_url.join('/');
        html = html+'<li><a href="'+url+'"">'+reserves_names[i]+'</a></li>';
    }
    $('#other_reserves_list').html(html);
}

function get_selected_days()
{
    var week_days = [];
    if ($("#id_seg").is(":checked"))
        week_days.push(0);
    if ($("#id_ter").is(":checked"))
        week_days.push(1);
    if ($("#id_qua").is(":checked"))
        week_days.push(2);
    if ($("#id_qui").is(":checked"))
        week_days.push(3);
    if ($("#id_sex").is(":checked"))
        week_days.push(4);
    if ($("#id_sab").is(":checked"))
        week_days.push(5);
    if ($("#id_dom").is(":checked"))
        week_days.push(6);
    return week_days;
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
