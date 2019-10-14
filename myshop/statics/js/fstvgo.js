//首页基本js
$(function() {

	$("#show_id").mouseenter(function() {
		$("#first_list").css("display", "block")
		$("#first_list").mouseleave(function() {
			$("#first_list").css("display", "none")
		})
	})

	$(".show_id").mouseenter(function() {
		$("#second_list").css("display", "block")
		$("#second_list").mouseleave(function() {
			$("#second_list").css("display", "none")
		})
	})

	
	$("img").mouseover(function(){
		$(this).animate({
		   opacity:0.7,
		},"fast")
		$(this).animate({
		   opacity:1,
		},"fast")
	})
})


$(function() {

	var bannerSlider = new Slider($('.c_show'), {
		time: 2500,
		delay: 400,
		event: 'click',
		auto: true,
		mode: 'fade',

	});

	var bannerSlidernum = new Slider($('.ico'), {
		time: 2500,
		delay: 400,
		event: 'click',
		auto: true,
		mode: 'fade',


	});

})


// 左边轮播图
$(function(){
	var box = $(".l_see");

	var ul = $(".l_ul");
	var size = $(".l_ul li").length;
	var i = 0;
	var timer = setInterval(function() {
		i++;
		move();
	}, 2700)

	function move() {
		if(i < 0) {
			ul.css("left", -(size - 1) * 208)
			i = size - 2
		}
		if(i >= size) {
			ul.css("left", 0);
			i = 1;
		}
		ul.stop().animate({
			left: -i * 208
		}, 800);
	}
	$("#left").click(function() {
		i--;
		move();
	})

	$("#right").click(function() {
		i++;
		move();
	})
})
	//	

//				var bannerSlider = new Slider($('.c_show'), {
//					time: 2500,
//					delay: 400,
//					event: 'click',
//					auto: true,
//					mode: 'fade',
//				    controller: $('.ico'),
//					activeControllerCls: 'active'
//				});

$(function() {
	var show = $(".c_list").find(".list_show");
	var li = $(".c_list_ul").children("li").mouseenter(function() {
		var _index = $(this).index();
		$(show).hide();
		$(show[_index]).show();
	});
	$("#cont").mouseleave(function() {
		$(show).hide();
	})

})

	//中间的轮播图
$(function() {
	var box = $("#mm_bb");
	var list1 = $("#mmm_bb #m_bb");
	var list2 = $("#mmm_bb");
	list1.first().clone().appendTo(list2);
	var sizes = $("#mmm_bb #m_bb").length;
	//console.log(sizes)

	var i = 0;
	var timer;

	function start() {
		timer = setInterval(function() {
			i++;
			move();
		}, 2500)
	}
	start();

	function move() {
		if(i < 0) {
			list2.css("left", -(sizes - 1) * 720)
			i = sizes - 2
		}
		if(i >= sizes) {
			list2.css("left", 0);
			i = 1;
		}
		list2.stop().animate({
			left: -i * 720
		}, 500);
	}
	$(".a_left").click(function() {
		clearInterval(timer)
		i--;
		move();
		start();
	})

	$(".a_right").click(function() {
		clearInterval(timer);
		i++;
		move();
		start();
	})
	$("#mm_bb").hover(function() {
			clearInterval(timer)
		},
		function() {
			clearInterval(timer);
			start();
		}
	)

})
//侧边导航栏
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
		// console.log($('body','html').scrollTop)
	    document.documentElement.scrollTop = 0
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


