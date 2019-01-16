$(function() {
	$(document).ready(function() {

		// Put listener
		$('.autocomplete').on('blur', function() {
			// Update selecter
			var text = $(this).val();
			$($(this).parent().parent().find('option')).each(function() {
	            if ($(this).text() === text) {
	                $(this).attr('selected', 'selected');
	            } else {
	                $(this).removeAttr('selected');
	            }
			});

		});
	});
});
