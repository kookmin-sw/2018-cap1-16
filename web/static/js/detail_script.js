        'use strict';

var $idxButtonForm = $('#idxButtonForm');

	$idxButtonForm.submit(function(e){
		e.preventDefault();
		var rowPerPage = 4;

		$('#nav').remove();

		var $ssdeepTable = $('#ssdeep_table');
		$ssdeepTable.after('<div id="nav">');


		var $ssdeepTr = $(ssdeep_table).find('tbody tr');

		var rowTotals = $ssdeepTr.length;
		var pageTotal = Math.ceil(rowTotals / rowPerPage);

		var i = 0;
		for(; i < pageTotal; i++){
			$('<a href="#"></a>')
				.attr('rel',i)
				.html(i+1)
				.appendTo('#nav');
		}

		$ssdeepTr.addClass('off-screen')
				.slice(0,rowPerPage)
				.removeClass('off-screen');

		var $pagingLink = $('#nav a');
		$pagingLink.on('click', function(evt){
			evt.preventDefault();
			var $this = $(this);
			if($this.hasClass('active')){
				return;
			}
			$pagingLink.removeClass('active');
			$this.addClass('active');

			
			var currPage = $this.attr('rel');
			var startItem = currPage * rowPerPage;
			var endItem = startItem + 4 ;
			$ssdeepTr.css('opacity','0.0')
				.addClass('off-screen')
				.slice(startItem,endItem)
				.removeClass('off-screen')
				.animate({opacity: 1}, 300);
		});

		$pagingLink.filter(':first').addClass('active');
	});
$idxButtonForm.submit();