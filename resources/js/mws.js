$(document).ready(function() {
	/* Core JS Functions */
	
	/* Collapsible Panels */
	$(".mws-panel.mws-collapsible .mws-panel-header")
		.append("<div class=\"mws-collapse-button mws-inset\"><span></span></div>")
			.find(".mws-collapse-button span")
				.live("click", function(event) {
					$(this).toggleClass("mws-collapsed")
						.parents(".mws-panel")
							.find(".mws-panel-body")
								.slideToggle("fast");
				});

	/* Side dropdown menu */
	$("div#mws-navigation ul li a, div#mws-navigation ul li span")
	.bind('click', function(event) {
		if($(this).next('ul').size() !== 0) {
			$(this).next('ul').slideToggle('fast', function() {
				$(this).toggleClass('closed');
			});
			event.preventDefault();
		}
	});
	
	/* Message & Notifications Dropdown */
	$("div#mws-user-tools .mws-dropdown-menu a").click(function(event) {
		$(".mws-dropdown-menu.toggled").not($(this).parent()).removeClass("toggled");
		$(this).parent().toggleClass("toggled");
		event.preventDefault();
	});
	
	$('html').click(function(event) {
		if($(event.target).parents('.mws-dropdown-menu').size() == 0) {
			$(".mws-dropdown-menu").removeClass("toggled");
		}
	});
	
	/* Side Menu Notification Class */
	$(".mws-nav-tooltip").addClass("mws-inset");
	
	/* Table Row CSS Class */
	$("table.mws-table tbody tr:even").addClass("even");
	$("table.mws-table tbody tr:odd").addClass("odd");
	
	/* File Input Styling */
	
	if($.fn.filestyle) {
		$("input[type='file']").filestyle({
			imagewidth: 78, 
			imageHeight: 28
		});
		$("input.file").attr("readonly", true);
	}
	
	/* Tooltips */
	
	if($.fn.tipsy) {
		var gravity = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
		for(var i in gravity)
			$(".mws-tooltip-"+gravity[i]).tipsy({gravity: gravity[i]});
			
		$('input[title], select[title], textarea[title]').tipsy({trigger: 'focus', gravity: 'w'});
	}
	
	/* Dual List Box */
	
	if($.configureBoxes) {
		$.configureBoxes();
	}
	
	if($.fn.placeholder) {
		$('[placeholder]').placeholder();
	}

    $('table.mws-datatable-fn tbody tr').on('click',function(e){
        if($(e.target).find('input[type="button"]').length == 0) {
            var check = $(this).find('input[type="checkbox"]');
            if(check.prop('checked')) {
                check.prop('checked',false);
                $(this).removeClass('table-tr-bg');
            }
            else {
                check.prop('checked',true);
                $(this).addClass('table-tr-bg');
            }
        }
    });
});

$.extend({
        StandardPost:function(url,args){
            var body = $(document.body),
                    form = $("<form method='post'></form>"),
                    input;
            form.attr({"action":url});
            $.each(args,function(key,value){
                input = $("<input type='hidden'>");
                input.attr({"name":key});
                input.val(value);
                form.append(input);
            });

            form.appendTo(document.body);
            form.submit();
            document.body.removeChild(form[0]);
        }
    });

