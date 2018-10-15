$(function(){
    start();
});

function start() {
    // Add listener to form fields
    $('.filter-option').on('click', function(e) {
        sendRequest($(this).attr('id'));
    });
    $('#filter-text').on('input', function() {
        $( ".filter-option" ).each(function( index ) {
            if (this.checked) {
                sendRequest($(this).attr('id'));
            }
        });
    });
}

// Send a request to get items according to typed filter
function sendRequest(filterType) {
    var csrftoken = getCookie('csrftoken');
    var filter = $("#filter-text").val();
    $.ajax({
        type: 'POST',
        url: '/faq/',
        data: {
            filterType: filterType,
            filter: filter,
            csrfmiddlewaretoken: csrftoken
        },
        dataType: 'json',
        success: function(data) {
            updateTable(data.faqItems);
        }
    });
}

// Show/hide faq items according to filter
function updateTable(faqItems) {
    $( ".faq-item" ).each(function( index ) {
        var itemTitle = $(this).find('.faq-title').html();
        if ($.inArray(itemTitle, faqItems) > -1) {
            $(this).css('display', 'table-row');
        } else {
            $(this).css('display', 'none');
        }
    });
}

// Function to get csrftoken to be used in server request
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