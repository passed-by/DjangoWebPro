$(function(){


	$(".p_center > div").mouseenter(function(){
		if ($(this).index() == 0) {
			$(this).eq(0).css({"background":"#ff5c4d","color":"white"});
		}else  {
			$(this).find("i").addClass("activess");
			$(this).find("b").stop().animate({right:"34px"}).css("background","#ff5c4d")
		}
	});
	$(".p_center div").mouseleave(function(){
		if ($(this).index() == 0) {
			$(this).eq(0).css({"background":"#333","color":"#ff5c4d"});
		}
		$(this).find("b").stop().animate({right:"-62px"}).css("background","#3f3c3c");
		$(this).find("i").removeClass("activess")
	})

	$(".p_foot div").mouseenter(function(){
		$(this).find("i").addClass("activess");
		$(this).find("img").show();
		$(this).find("b").animate({right:"34px"}).css("background","#ff5c4d")

	})
	$(".p_foot div").mouseleave(function(){
		$(this).find("b").animate({right:"-62px"}).css("background","#3f3c3c");
		$(this).find("i").removeClass("activess")
		$(this).find("img").hide();
	})


	    //var scrollTop = $("body").scrollTop();
	    //console.log(scrollTop);
	$("#totop").click(function(){
		console.log($('body','html').scrollTop)
	    $('body','html').animate({
			scrollTop:0
		},200);
		return false;
	})


	$(window).scroll(function(){
		var scrollTop = $(this).scrollTop();
	    if(scrollTop >= 640){
		  $("#dock").show();
		}else if(scrollTop<640){
		  $("#dock").hide();
		}
	})

})