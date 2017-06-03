$(function() {
	/**
	 * jquery方法：addClass() addClass() 方法向被选元素添加一个或多个类。该方法不会移除已存在的 class
	 * 属性，仅仅添加一个或多个 class 属性。 如需添加多个类，请使用空格分隔类名。
	 */
	$("#login").addClass("current");

	/**
	 * 正则检验邮箱 email 传入邮箱 return true 表示验证通过
	 */
	function check_email(email) {
		if (/^[\w\-\.]+@[\w\-]+(\.[a-zA-Z]{2,4}){1,2}$/.test(email)) {
			return true;
		}
	}

	/**
	 * input 按键事件keyup
	 */
	$("input[name]").keyup(function(e) {
		// 禁止输入空格 把空格替换掉(空格的ASCII为32)
		if ($(this).attr('name') == "password" && e.keyCode == 32) {
			$(this).val(function(i, v) {
				return $.trim(v);
			});
		}
		if ($.trim($(this).val()) != "") {
			$(this).nextAll('span').eq(0).css({
				display : 'none'
			});
		}
	});

	// 错误信息
	var succ_arr = [];

	/**
	 * input失去焦点事件focusout 这跟blur事件区别在于，他可以在父元素上检测子元素失去焦点的情况。
	 */
	$("input[name]").focusout(function(e) {
		var msg = "";
		if ($.trim($(this).val()) == "") {
			if ($(this).attr('name') == 'username') {
				succ_arr[0] = false;
				msg = "Input Username";
			} else if ($(this).attr('name') == 'password') {
				succ_arr[1] = false;
				msg = "Input Password";
			}
		} else {
			if ($(this).attr('name') == 'username') {
				succ_arr[0] = true;
			} else if ($(this).attr('name') == 'password') {
				succ_arr[1] = true;
			}
		}
		$(this).nextAll('span').eq(0).css({
			display : 'block'
		}).text(msg);
	});

	/**
	 * Ajax用户注册
	 */
	$("button[type='button']").click(function() {
		$("input[name]").focusout(); // 让所有的input标记失去一次焦点来设置msg信息
		for (x in succ_arr) {
			if (succ_arr[x] == false)
				return;
		}

		$("span[name='error_message']").eq(0).css({
						display : 'block'
					}).text('');
		var data = $('#login').serialize(); // 序列化表单元素

		$.ajax({
			type: 'POST',
			url : "/auth/valid_login",
			data : data,
			success : function(result) {
				if (result.success) {
					window.location = result.redirect;
				} else {
					$("span[name='username']").eq(0).css({
						display : 'block'
					}).text(result.errors.username);
					$("span[name='password']").eq(0).css({
						display : 'block'
					}).text(result.errors.password);
				}
			},
			error : function(result) {
				$("span[name='error_message']").eq(0).css({
						display : 'block'
					}).text('Server Exception');
			}
		});

		/**
		 * 有兴趣的可以到这里 自行发送Ajax请求 实现注册功能
		 */
	});

});


$(document).ready(function() {
    
	STATIC_ROOT = 'http://' + window.location.host + '/static';
	$.get( STATIC_ROOT+"/libs/extjs/ext-all.js");
	$.get( STATIC_ROOT+"/libs/extjs/theme-triton/theme-triton.js");
	$.get( STATIC_ROOT+"/libs/extjs/theme-triton/resources/theme-triton-all.css");
});