$(function(){
	$(document).ready(function () {
		updateLabels();
	});
});

function updateLabels() {
	$('.selector-available').each(function() {
		var label = $(this).parent().parent().children('label').text().toLowerCase();
		$(this).children('input').attr('placeholder', 'Digite aqui '+label+' desejados');
		var input = $(this).children('input')[0].outerHTML;
		$(this).children('input').remove();
		$(this).prepend('<div class="filtered-search"><i class="material-icons">search</i>'+input+'</div>');
		$('</div>').insertAfter($(this).children('input'));
		addListener();

		$(this).parent().children('.selector-chosen').children('input').attr('placeholder', label+' escolhido(s)');
	});
}

function addListener() {
	$('.filtered-search').children('input').on('input', function() {
		var typed = $(this).val().toLowerCase();
		var options = $(this).parent().parent().children('.filtered').children('option');
		$(options).each(function() {
			if ($(this).text().toLowerCase().search(typed) == -1) {
				$(this).css('display', 'none');
			} else {
				$(this).css('display', '');
			}
		});
	});
}