$(function() {

	var ul_li = $(".g_show ul").length
	var index = 0;
	move();
	$(".g_show li").click(function() {
		index = $(this).index();
		move();
	})

	function move() {
		$(".g_show li").eq(index).find("img").addClass("active1").parent().siblings().find("img").removeClass("active1");
		$(".gl_pic").animate({
			"left": -(480 * index)
		}, 100)
		var src = $(".g_show li").eq(index).find("img").attr("src");
		var bigpic = $("<img src=" + src + "/>");
		bigpic.appendTo($("#boost"));
		bigpic.siblings().remove("img")
			//console.log(bigpic)

		if(index >= 3 && index <= 4) {
			$(".g_show ul").animate({
				"left": -(62 * (index - 2))
			}, 200)
		}
		if($(".g_show ul").position().left < 0 && index == 2) {
			$(".g_show ul").animate({
				"left": -(62 * (index - 2))
			}, 170)
		}
		glee();
	}
	$('.gleft').click(function() {
		if (ul_li == 1) {
			return false
		}
		index = $("img.active1").parent().index();
		index--;
		if(index <= 0) {
			index = 0;
		}
		move();
	})
	$('.gright').click(function() {
		if (ul_li == 1) {
			return false
		}
		index = $("img.active1").parent().index();
		index++;
		if(index >= 6) {
			index = 6;
		}
		move();
	})
		//放大镜
	glee();

	function glee() {
		var smlpic = $(".gl_big");
		var smlare = $("#smlare");
		var bigpic = $("#boost img");
		//console.log(bigpic)
		var bigare = $("#boost");
		smlare.width(smlpic.width() / bigpic.width() * bigare.width())
		smlare.height(smlpic.height() / bigpic.height() * bigare.width())
		var scal = bigpic.width() / smlpic.width();
		smlpic.mousemove(function(e) {
			bigare.show();
			smlare.show();
			var x = e.pageX - smlare.offset().left - smlare.width() / 2;
			var y = e.pageY - smlare.offset().top - smlare.height() / 2;
			//console.log(x)
			if(x < 0) {
				x = 0;
			} else if(x > smlpic.width() - smlare.width()) {
				x = smlpic.width() - smlare.width()
			}
			if(y < 0) {
				y = 0;
			} else if(y > smlpic.height() - smlare.height()) {
				y = smlpic.height() - smlare.height()
			}
			smlare.css({
				left: x,
				top: y,
			});
			bigpic.css({
				left: -(x * scal),
				top: -(y * scal)
			})
		})
		smlpic.mouseleave(function() {
			bigare.hide();
			smlare.hide();
		})
	}

})
$(function() {
	var show = $(".cc_list").find(".list_show");
	$(".f_li").mouseenter(function() {
		$(".cc_list").show();
		$(".c_list_ul").children("li").mouseenter(function() {
			var _index = $(this).index();
			$(show).hide();
			$(show[_index]).show();
		});

	})
	$("#contents").mouseleave(function() {
		$(show).hide();
		$(".cc_list").hide();
	})
	$(".tab li").click(function() {
		$(this).addClass("on");
		$(this).siblings().removeClass("on");
		var i = $(this).index();
		$("#box div").eq(i).show().siblings().hide();

	})

	$(".box1 h2:even").css({
		"background": "#faf3f0",
		"line-height": "28px"
	});
	$(".box1 h2:odd").css({
		"font-weight": "normal",
		"line-height": "1.5"
	});

})