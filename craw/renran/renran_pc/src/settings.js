export default {
  Host:"http://api.renran.cn:8000",
  TC_captcha:{
    app_id: "2072894469",
  },

  save_user(storage, data){
    if(storage === sessionStorage){
      var storage2 = localStorage;
    }else{
      var storage2 = sessionStorage;
    }

    storage2.removeItem("user_token");
    storage2.removeItem("user_name");
    storage2.removeItem("user_id");
    storage2.removeItem("user_nickname");
    storage2.removeItem("user_avatar");

    storage.user_token = data.token;
    storage.user_name = data.username;
    storage.user_id = data.id;
    storage.user_nickname = data.nickname;
    storage.user_avatar = data.avatar;
  },
  jump_page(vm,message, title="登陆成功",confirm_text="个人中心",confirm_url="/user", cancel_text="返回上一页"){
    vm.$confirm(message, title, {
      confirmButtonText: confirm_text,
      cancelButtonText: cancel_text,
      type: 'success'
    }).then(() => {
      // 跳转到个人中心
      vm.$router.push(confirm_url);
    }).catch(() => {
      // 跳转到上一页
      vm.$router.back();
    });
  },
  check_user_login(vm){
    // 判断用户是否已经登陆
    let token = localStorage.user_token || sessionStorage.user_token;
    if(!token){
      // 跳转到登陆页面
      this.jump_page(vm, "尊敬的游客, 您尚未登陆!请登陆后再进行操作!", "警告","去登陆", "/user/login");
    }

    return token;
  }
}

