$(function() {
	$(document).ready(function() {
	    $('form input').each(function() {
	        if (($(this).attr('type') === 'checkbox') && ($(this).attr('readonly'))) {
	        	alert($(this).attr('id'));
	            $(this).off();
	        }
	    });
	});
});