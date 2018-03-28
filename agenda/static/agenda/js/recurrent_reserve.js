var hidden = true;

$(function()
{
    $(document).ready(function() {
        prevent_default_submit();
        initialize_date_inputs();
        var question_mark = create_and_return_questionmark();
        add_tooltip(question_mark);
        add_listeners_to_option();
    });
});

function prevent_default_submit() {
    var submit_button = $(".submit-row input");
    submit_button.on("click", function( event ) {
        if (!hidden)
        {
            event.preventDefault();
            create_confirmation_modal();
            update_modal_dates();
            open_modal();
        }
    });
}

function open_modal() {
    $( "#dialog-confirm" ).dialog({
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
        "Concordar": function() {
            $('form').submit();
        },
        "Cancelar": function() {
            $( this ).dialog( "close" );
        }
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
    $('.field-dataInicio').css('display', 'initial');
    $('.field-dataFim').css('display', 'initial');
    $('.field-seg').css('display', 'initial');
    $('.field-ter').css('display', 'initial');
    $('.field-qua').css('display', 'initial');
    $('.field-qui').css('display', 'initial');
    $('.field-sex').css('display', 'initial');
    $('.field-sab').css('display', 'initial');
    $('.field-dom').css('display', 'initial');
    hidden = false;
}

function hide_date_inputs()
{
    $('.field-dataInicio').css('display', 'none');
    $('.field-dataFim').css('display', 'none');
    $('.field-seg').css('display', 'none');
    $('.field-ter').css('display', 'none');
    $('.field-qua').css('display', 'none');
    $('.field-qui').css('display', 'none');
    $('.field-sex').css('display', 'none');
    $('.field-sab').css('display', 'none');
    $('.field-dom').css('display', 'none');
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
        <div id="dialog-confirm" title="Reserva Recorrente">
            <p>Essa é uma reserva recorrente, alterações aqui feitas terão efeito nas reservas recorrentes do dia <span id="starting_date"></span> ao dia <span id="ending_date"></span>.<p>
                Caso deseje editar apenas essa reserva, certifique-se de que a opção "Recorrente" está desmarcada.</p>
        </div>
    `
    $('form').append(modal_html);
}