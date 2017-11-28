$(function() {
	var hour_options = ['07', '08', '09', '10', '11', '11', '13', '14', '15', '16', '17', '18', '18', '19', '20', '21', '22'];
	var minute_options = ['30', '20', '10', '10', '00', '50', '30', '20', '10', '20', '10', '00', '30', '20', '20', '10', '00'];
	var options_html = "";

	$(document).ready(function(){
		for (i = 0; i < hour_options.length; i++) {
			var hour = hour_options[i];
			var minute = minute_options[i];
			options_html += "<div class='xdsoft_time' data-hour='" + hour + "' data-minute='" + minute + "'>" + hour + ":" + minute +"</div>";
		}
		$(".xdsoft_time_variant").on("DOMSubtreeModified", function() {
			$(this).html(options_html);
		});

	});
});