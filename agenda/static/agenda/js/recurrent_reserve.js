var hidden = false;

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
    if (!$("#id_recorrente").attr('checked')) {
        hide_date_inputs();
    }
}

function add_listeners_to_option()
{
    $('#id_recorrente').on("click", function() {
        if (hidden)
        {
            $('#id_dataInicio_container').css('display', '');
            $('#id_dataFim_container').css('display', '');
            hidden = false;
        }
        else
        {  
            hide_date_inputs();
        }
    });
}

function hide_date_inputs()
{
    $('#id_dataInicio_container').css('display', 'none');
    $('#id_dataFim_container').css('display', 'none');
    hidden = true;
}

function add_tooltip(question_mark)
{
    var tooltip_text = `
        Reserva recorrente cria reservas em todos os dias da semana<br>
        iguais à data selecionada entre certo período.<br>
        <br>
        Ex: Todas as segundas, das 10:00 às 11:00, de 23/01/18 até 23/06/18.
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
        $('form').submit();
    });
}