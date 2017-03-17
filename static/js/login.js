$(function(){
	var $avatar_exist = $('.avatar_exist');
	var $no_avatar = $('.no_avatar');
	var $notlogin = $('.notlogin');

	var $exit = $('#exit');
	var $login = $('#login');
	var $register = $('#register');

	$.get({
		url:'/user/islogin',
		type:'GET',
		dataType:'json'
	})
	.done(function(dat){
		if (dat.status == 0){
			$notlogin.show();
			$avatar_exist.prop({href:''});
			$avatar_exist.hide();
			$no_avatar.prop({href:''});
			$no_avatar.hide();
			
			$exit.hide();
			$login.show();
			$register.show();
		}
		else{
			var href = '/user/userinfo/' + dat.info.name;
			if(dat.info.avatar){
				$avatar_exist.show();
				$avatar_exist.prop({href:href});
				$no_avatar.hide();
			}
			else{
				$no_avatar.show();
				$no_avatar.prop({href:href});
				$avatar_exist.hide();
			}
			$notlogin.hide();
			$exit.show();
			$login.hide();
			$register.hide();
			
		}
	})
})