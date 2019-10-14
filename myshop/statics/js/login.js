$(function() {
	$("#getup").click(function() {
		var users = $.cookie("users");
		console.log(users)
		console.log(users)
		var isExists = false;
		if(users) {
			isExists = true;
			var isexistrs = false;
			users = JSON.parse(users);
			for(i = 0; i < users.length; i++) {
				if(users[i].phone == $(".user").val() && users[i].key == $(".uerschake").val()) {
					
					//保存登录的用户
					var loginUser = {name:$(".user").val(), pwd:$(".uerschake").val()}
					$.cookie("loginUser", JSON.stringify(loginUser), {expires:22, path:"/"})
					
					window.location.href = "index.html";
					isexistrs = true;
				}
			}
			if(!isexistrs) {
				if($(".user").val() == 0) {
					alert("请输入用户名或密码")
				} else {
					alert("用户名或密码错误")
				}
			}
		}
		if(!isExists) {
			alert("请注册")
		}
	})
})