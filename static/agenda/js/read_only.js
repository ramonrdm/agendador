$(function() {
	$(document).ready(function() {
	    $('form input').each(function() {
	        if (($(this).attr('type') === 'checkbox') && ($(this).attr('readonly'))) {
	            $(this).off();
	        }
	    });
	});
});