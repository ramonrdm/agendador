$(function() {
	var input = '.ufsc_time';
	jQuery(input).datetimepicker({
		datepicker:false,
		format:'H:i',
		allowTimes:[
			'7:30', '8:20', '9:10', '10:10', '11:00', '11:50', 
			'13:30', '14:20', '15:10', '16:20', '17:10', '18:00',
			'18:30', '19:20', '20:20', '21:10', '22:00'
		],
		onShow:function(ct,$i){
	  		input = $i;
	  		$('#yourElement').blur();
		},
	});

	//  check if mobile browser
	if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
		$('.xdsoft_time_variant').unbind('click');
		$('.xdsoft_time_variant').unbind('touchend');
		$('.xdsoft_time_variant').unbind('touchmove');
		$('.xdsoft_time_variant').unbind('touchstart'); 
		$('.xdsoft_time_variant').unbind('touchcancel'); 
		startResponsive();
	}

	function startResponsive() {
		var clicked = false, clickY;
		var select = true;
		$(".xdsoft_time_box").on({
		    'touchmove': function(e) {
		    	select = false;
		        clicked && updateScrollPos(e);
		    },
		    'mousedown': function(e) {
		        clicked = true;
		        clickY = e.pageY;
		    },
		    'touchend': function(e) {
		        if (select) {
		        	var target = $(e.target);
			        var selection_box = $(e.target).closest(".xdsoft_datetimepicker");
			        selection_box.css('display', 'none');
			        $(input).val(target.text());
		        }
		        select = true;
		    }
		});

		$(document).on({
		    'mouseup': function() {
		        clicked = false;
		        select = true;
		        $('html').css('cursor', 'auto');
		    }
		});

		var updateScrollPos = function(e) {
			// update div
		    var new_position = ($(".xdsoft_time_variant").css("margin-top"));
		    new_position = Number(new_position.slice(0, -2));  // make the value an integer
		    new_position = new_position - ((clickY - e.pageY) * 0.1);  // roll speed
			var max = $('.xdsoft_time_variant').height() - $('.xdsoft_time_box').height();
		    // for some reason sometime the operation below will result in negative,
		    // set the max for this case
			if (max < 0) {
				max = $('.xdsoft_time_box').height() - max - $('.xdsoft_time ').height();
			}
			// can't go above or below the options
		    if ((-new_position) > max)
		    {
		    	new_position = -max;
		    }
		    else if (new_position > 0)
		    {
		    	new_position = 0;
		    }
		    new_position = "" + new_position + "px";
		    $(".xdsoft_time_variant").css("margin-top", new_position);
		}


		$('.xdsoft_scrollbar').css('display', 'none');
	}
});