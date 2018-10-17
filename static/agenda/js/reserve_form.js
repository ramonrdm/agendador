$(function(){
    $(document).ready(function() {
        var initial_status = $('#id_estado').val();
        var current_url = window.location.href;
		init_modal();
		create_listener();
	});
});

function init_modal()  {
    $('#confirmation-modal').modal({endingTop: '30%'});
    $("#submit_button_create_modal").on("click", function() {
        $('form').submit();
    });
}

function update_modal(reserves_ids, reserves_names) {
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

function check_reserves(reservable_type, reservable_name, date, starting_time, ending_time){
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
            starting_time: starting_time,
            ending_time: ending_time,
            current_reserve_id: current_reserve_id,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
        success: function(data) {
            if (data.conflict_reserves) {
                update_modal_dates();
                update_modal(data.conflict_reserves_ids, data.conflict_reserves_names)
                $("#confirmation-modal").modal('open');
            } else {
                $('form').submit();
            }
        }
    });
}

function create_listener() {
    var submit_button = $(".right-align").find('button:first');
    submit_button.on("click", function( event ) {
        var status = $('#id_estado').val();
        if ((status == 'A') && (! $("#id_recorrente").is(":checked"))) {
            event.preventDefault();
            var reservable_type = $('.page-title').text();
            var reservable_name = $('#id_locavel').parent().children('.select-dropdown').attr('value');
            var date = $('#id_data').val();
            var starting_time = $('#id_horaInicio').val();
            var ending_time = $('#id_horaFim').val();
            check_reserves(reservable_type, reservable_name, date, starting_time, ending_time);
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