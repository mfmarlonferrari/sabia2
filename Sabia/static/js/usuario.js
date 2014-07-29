$(function(){
	$(".dropdown-menu li a").click(function(){		
		$(this).parents(".btn-group").find('.btn-text').text($(this).text());		
		// Insere o id do grupo no campo hidden
		$('#grupo_id').val($(this).data('value'));
	});
});
