<template>
    <div v-show="show_page">
      <div class="sign">
        <div class="logo"><a href="/"><img src="/static/image/nav-logo.png" alt="Logo"></a></div>
        <div class="main">
          <h4 class="title">
            <div class="normal-title">
                <a :class="status==1?'active':''" @click="status=1">已有账号</a>
                <b>·</b>
                <a :class="status==2?'active':''" @click="status=2">没有账号</a>
            </div>
          </h4>
          <div class="js-sign-in-container" v-if="status==1">
            <form action="" method="post">
                <div class="input-prepend restyle js-normal">
                  <input placeholder="登录账号或手机号或邮箱" type="text" v-model="username">
                  <i class="iconfont ic-user"></i>
                </div>
                <div class="input-prepend">
                  <input placeholder="密码" type="password" v-model="password">
                  <i class="iconfont ic-password"></i>
                </div>
                <div class="forget-btn">
                  <router-link to="/find_password">通过邮箱找回密码?</router-link>
                </div>
                <button class="sign-in-button" type="button" @click.prevent="show_captcha">
                  <span></span>登录
                </button>
            </form>
          </div>
          <div class="js-sign-in-container" v-if="status==2">
            <form class="new_user" id="new_user" action="" accept-charset="UTF-8" method="post">
              <div class="input-prepend restyle">
                  <input placeholder="你的昵称" type="text" value="" v-model="nickname" id="user_nickname">
                <i class="iconfont ic-user"></i>
              </div>
                <div class="input-prepend restyle no-radius js-normal">
                    <input placeholder="手机号" type="tel" v-model="mobile" id="user_mobile_number">
                  <i class="iconfont ic-phonenumber"></i>
                </div>
              <div class="input-prepend restyle no-radius security-up-code js-security-number" v-if="is_show_sms_code">
                  <input type="text" v-model="sms_code" id="sms_code" placeholder="手机验证码">
                <i class="iconfont ic-verify"></i>
                <a tabindex="-1" class="btn-up-resend js-send-code-button"  href="javascript:void(0);" id="send_code" @click.prevent="send_sms">{{sms_code_text}}</a>
              </div>
              <input type="hidden" name="security_number" id="security_number">
              <div class="input-prepend">
                <input placeholder="设置密码" type="password" v-model="password" id="user_password">
                <i class="iconfont ic-password"></i>
              </div>
              <input type="submit" name="commit" value="注册" class="sign-up-button" id="sign_up_btn" @click.prevent="registerHandler">
              <p class="sign-up-msg">点击 “注册” 即表示您同意并愿意遵守荏苒<br> <a target="_blank" href="">用户协议</a> 和 <a target="_blank" href="">隐私政策</a> 。</p>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
    export default {
        name: "QQCallBack",
        data(){
          return {
              show_page: false,
              status: 1, // 当前用户是否拥有了平台账号
              username: "",
              password: "",
              nickname:"",
              mobile:"",
              sms_code:"",
              sms_code_text:"发送验证码",
              is_show_sms_code:false,
              qq_user:"", // qq用户的相关信息
          }
        },
        created(){
            this.get_user_info();
        },
        methods:{
            get_user_info(){
                // 转发code提供给服务端
                this.$axios.get(`${this.$settings.Host}/oauth/qq/info/`+location.search
                ).then(response=>{
                   if(response.data.token){
                      // 当前用户有账号并且属于非第一次QQ登陆
                      this.$settings.save_user(sessionStorage, response.data);
                      this.$settings.jump_page(this, response.data.nickname);
                   }else{
                       // 当前用户属于第一次QQ登陆,显示账号绑定页面
                       this.show_page = true; // 界面内容显示出来
                       this.qq_user = response.data;
                   }
                }).catch(error=>{
                   this.$message.error("网络错误!无法使用QQ第三方登陆");
                });
            },
            show_captcha(){
                // 显示验证码

                if(this.username.length<1 || this.password.length<1){
                    this.$message.error("对不起,账号或密码不能为空!");
                    return ;
                }

                var captcha1 = new TencentCaptcha(this.$settings.TC_captcha.app_id, res=>{
                    /*
                    * ret	      Int	      验证结果，0：验证成功。2：用户主动关闭验证码。
                      ticket	  String	  验证成功的票据，当且仅当 ret = 0 时 ticket 有值。
                      appid	    String	  场景 ID。
                      bizState	Any	      自定义透传参数。
                      randstr	  String	 本次验证的随机串，请求后台接口时需带上。
                    *
                    * */
                    if(res.ret === 0){
                      this.$axios.post(`${this.$settings.Host}/users/captcha/`,{
                          ret: res.ret,
                          ticket: res.ticket,
                          randstr: res.randstr,
                      }).then(response=>{
                          if(response.data.message && response.data.randstr === res.randstr){
                              // 验证成功
                              this.loginHandler();
                          }else{
                              this.$meesage.error("验证码验证失败!请重新操作验证码");
                              captcha1.destroy();
                          }
                      }).catch(error=>{
                          console.log("发生错误!", error);
                      })
                    }
                });
                captcha1.show();
            },
            loginHandler(){
                // 登陆账号完成QQ的绑定
                this.$axios.put(`${this.$settings.Host}/oauth/qq/info/`,{
                    username: this.username,
                    password: this.password,
                    qq_user: this.qq_user,
                }).then(response=>{
                    this.$settings.save_user(sessionStorage, response.data);
                    this.$settings.jump_page(this, `${response.data.nickname},欢迎来到荏苒!`);
                }).catch(error=>{
                    this.$message.error(error.response.data);
                });
            },
            registerHandler(){
                // 注册账号完成QQ的绑定
                this.$axios.post(`${this.$settings.Host}/oauth/qq/info/`,{
                    nickname: this.nickname,
                    password: this.password,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    qq_user: this.qq_user,
                }).then(response=>{
                    this.$settings.save_user(sessionStorage, response.data);
                    this.$settings.jump_page(this, `${response.data.nickname},欢迎来到荏苒!`);
                }).catch(error=>{
                    this.$message.error("绑定QQ账号失败!"+error.response.data);
                });
            }
        }
    }
</script>

<style scoped>
input{
  outline: none;
}
*, :after, :before {
    box-sizing: border-box;
}
.sign {
	height: 100%;
	min-height: 750px;
	text-align: center;
	font-size: 14px;
	background-color: #f1f1f1
}

.sign:before {
	content: "";
	display: inline-block;
	height: 85%;
	vertical-align: middle
}

.sign .disable,.sign .disable-gray {
	opacity: .5;
	pointer-events: none
}

.sign .disable-gray {
	background-color: #969696
}

.sign .tooltip-error {
	font-size: 14px;
	line-height: 25px;
	white-space: nowrap;
	background: none
}

.sign .tooltip-error .tooltip-inner {
	max-width: 280px;
	color: #333;
	border: 1px solid #ea6f5a;
	background-color: #fff
}

.sign .tooltip-error .tooltip-inner i {
	position: static;
	margin-right: 5px;
	font-size: 20px;
	color: #ea6f5a;
	vertical-align: middle
}

.sign .tooltip-error .tooltip-inner span {
	vertical-align: middle;
	display: inline-block;
	white-space: normal;
	max-width: 230px
}

.sign .tooltip-error.right .tooltip-arrow-border {
	border-right-color: #ea6f5a
}

.sign .tooltip-error.right .tooltip-arrow-bg {
	left: 2px;
	border-right-color: #fff
}

.sign .slide-error {
	position: relative;
	padding: 10px 0;
	border: 1px solid #c8c8c8;
	border-radius: 4px
}

.sign .slide-error i {
	position: static!important;
	margin-right: 10px;
	color: #ea6f5a!important;
	vertical-align: middle
}

.sign .slide-error span {
	font-size: 15px;
	vertical-align: middle
}

.sign .slide-error div {
	margin-top: 10px;
	font-size: 13px
}

.sign .slide-error a {
	color: #3194d0
}

.sign .js-sign-up-forbidden {
	color: #999;
	padding: 80px 0 100px
}

.sign .js-sign-up-container .slide-error {
	border-bottom: none;
	border-radius: 0
}

.sign .logo {
	position: absolute;
	top: 56px;
	margin-left: 50px
}

.sign .logo img {
	width: 100px
}

.sign .main {
	width: 400px;
	margin: 60px auto 0;
	padding: 50px 50px 30px;
	background-color: #fff;
	border-radius: 4px;
	box-shadow: 0 0 8px rgba(0,0,0,.1);
	vertical-align: middle;
	display: inline-block
}

.sign .reset-title,.sign .title {
	margin: 0 auto 50px;
	padding: 10px;
	font-weight: 400;
	color: #969696
}

.sign .reset-title a,.sign .title a {
	padding: 10px;
	color: #969696
}

.sign .reset-title a:hover,.sign .title a:hover {
	border-bottom: 2px solid #ea6f5a
}

.sign .reset-title .active,.sign .title .active {
	font-weight: 700;
	color: #ea6f5a;
	border-bottom: 2px solid #ea6f5a
}

.sign .reset-title b,.sign .title b {
	padding: 10px
}

.sign .reset-title {
	color: #333;
	font-weight: 700
}

.sign form {
	margin-bottom: 30px
}

.sign form .input-prepend {
	position: relative;
	width: 100%
}

.sign form .input-prepend input {
	width: 100%;
	height: 50px;
	margin-bottom: 0;
	padding: 4px 12px 4px 35px;
	border: 1px solid #c8c8c8;
	border-radius: 0 0 4px 4px;
	background-color: hsla(0,0%,71%,.1);
	vertical-align: middle
}

.sign form .input-prepend i {
	position: absolute;
	top: 14px;
	left: 10px;
	font-size: 18px;
	color: #969696
}

.sign form .input-prepend span {
	color: #333
}

.sign form .input-prepend .ic-show {
	top: 18px;
	left: auto;
	right: 8px;
	font-size: 12px
}

.sign form .geetest-placeholder {
	height: 44px;
	border-radius: 4px;
	background-color: hsla(0,0%,71%,.1);
	text-align: center;
	line-height: 44px;
	font-size: 14px;
	color: #999
}

.sign form .restyle {
	margin-bottom: 0
}

.sign form .restyle input {
	border-bottom: none;
	border-radius: 4px 4px 0 0
}

.sign form .no-radius input {
	border-radius: 0
}

.sign form .slide-security-placeholder {
	height: 32px;
	background-color: hsla(0,0%,71%,.1);
	border-radius: 4px
}

.sign form .slide-security-placeholder p {
	padding-top: 7px;
	color: #999;
	margin-right: -7px
}

.sign .overseas-btn {
	font-size: 14px;
	color: #999
}

.sign .overseas-btn:hover {
	color: #2f2f2f
}

.sign .remember-btn {
	float: left;
	margin: 15px 0
}

.sign .remember-btn span {
	margin-left: 5px;
	font-size: 15px;
	color: #969696;
	vertical-align: middle
}

.sign .forget-btn {
	float: right;
	position: relative;
	margin: 15px 0;
	font-size: 14px
}

.sign .forget-btn a {
	color: #999
}

.sign .forget-btn a:hover {
	color: #333
}

.sign .forget-btn .dropdown-menu {
	top: 20px;
	left: auto;
	right: 0;
	border-radius: 4px
}

.sign .forget-btn .dropdown-menu a {
	padding: 10px 20px;
	color: #333
}

.sign #sign-in-loading {
	position: relative;
	width: 20px;
	height: 20px;
	vertical-align: middle;
	margin-top: -4px;
	margin-right: 2px;
	display: none
}

.sign #sign-in-loading:after {
	content: "";
	position: absolute;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background-color: transparent
}

.sign #sign-in-loading:before {
	content: "";
	position: absolute;
	top: 50%;
	left: 50%;
	width: 20px;
	height: 20px;
	margin: -10px 0 0 -10px;
	border-radius: 10px;
	border: 2px solid #fff;
	border-bottom-color: transparent;
	vertical-align: middle;
	-webkit-animation: rolling .8s infinite linear;
	animation: rolling .8s infinite linear;
	z-index: 1
}

.sign .sign-in-button,.sign .sign-up-button {
	margin-top: 20px;
	width: 100%;
	padding: 9px 18px;
	font-size: 18px;
	border: none;
	border-radius: 25px;
	color: #fff;
	background: #42c02e;
	cursor: pointer;
	outline: none;
	display: block;
	clear: both
}

.sign .sign-in-button:hover,.sign .sign-up-button:hover {
	background: #3db922
}

.sign .sign-in-button {
	background: #3194d0
}

.sign .sign-in-button:hover {
	background: #187cb7
}

.sign .btn-in-resend,.sign .btn-up-resend {
	position: absolute;
	top: 7px;
	right: 7px;
	width: 100px;
	height: 36px;
	font-size: 13px;
	color: #fff;
	background-color: #42c02e;
	border-radius: 20px;
	line-height: 36px
}

.sign .btn-in-resend {
	background-color: #3194d0
}

.sign .sign-up-msg {
	margin: 10px 0;
	padding: 0;
	text-align: center;
	font-size: 12px;
	line-height: 20px;
	color: #969696
}

.sign .sign-up-msg a,.sign .sign-up-msg a:hover {
	color: #3194d0
}

.sign .overseas input {
	padding-left: 110px!important
}

.sign .overseas .overseas-number {
	position: absolute;
	top: 0;
	left: 0;
	width: 100px;
	height: 50px;
	font-size: 18px;
	color: #969696;
	border-right: 1px solid #c8c8c8
}

.sign .overseas .overseas-number span {
	margin-top: 17px;
	padding-left: 35px;
	text-align: left;
	font-size: 14px;
	display: block
}

.sign .overseas .dropdown-menu {
	width: 100%;
	max-height: 285px;
	font-size: 14px;
	border-radius: 0 0 4px 4px;
	overflow-y: auto
}

.sign .overseas .dropdown-menu li .nation-code {
	width: 65px;
	display: inline-block
}

.sign .overseas .dropdown-menu li a {
	padding: 6px 20px;
	font-size: 14px;
	line-height: 20px
}

.sign .overseas .dropdown-menu li a::hover {
	color: #fff;
	background-color: #f5f5f5
}

.sign .more-sign {
	margin-top: 50px
}

.sign .more-sign h6 {
	position: relative;
	margin: 0 0 10px;
	font-size: 12px;
	color: #b5b5b5
}

.sign .more-sign h6:before {
	left: 30px
}

.sign .more-sign h6:after,.sign .more-sign h6:before {
	content: "";
	border-top: 1px solid #b5b5b5;
	display: block;
	position: absolute;
	width: 60px;
	top: 5px
}

.sign .more-sign h6:after {
	right: 30px
}

.sign .more-sign ul {
	margin-bottom: 10px;
	list-style: none
}

.sign .more-sign ul li {
	margin: 0 5px;
	display: inline-block
}

.sign .more-sign ul a {
	width: 50px;
	height: 50px;
	line-height: 50px;
	display: block
}

.sign .more-sign ul i {
	font-size: 28px
}

.sign .more-sign .ic-weibo {
	color: #e05244
}

.sign .more-sign .ic-wechat {
	color: #00bb29
}

.sign .more-sign .ic-qq_connect {
	color: #498ad5
}

.sign .more-sign .ic-douban {
	color: #00820f
}

.sign .more-sign .ic-more {
	color: #999
}

.sign .more-sign .weibo-loading {
	pointer-events: none;
	cursor: pointer;
	position: relative
}

.sign .more-sign .weibo-loading:after {
	content: "";
	position: absolute;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background-color: #fff
}

body.reader-night-mode .sign .more-sign .weibo-loading:after {
	background-color: #3f3f3f
}

.sign .more-sign .weibo-loading:before {
	content: "";
	position: absolute;
	top: 50%;
	left: 50%;
	width: 20px;
	height: 20px;
	margin: -10px 0 0 -10px;
	border-radius: 10px;
	border: 2px solid #e05244;
	border-bottom-color: transparent;
	vertical-align: middle;
	-webkit-animation: rolling .8s infinite linear;
	animation: rolling .8s infinite linear;
	z-index: 1
}

@keyframes rolling {
	0% {
		-webkit-transform: rotate(0deg);
		transform: rotate(0deg)
	}

	to {
		-webkit-transform: rotate(1turn);
		transform: rotate(1turn)
	}
}

@-webkit-keyframes rolling {
	0% {
		-webkit-transform: rotate(0deg)
	}

	to {
		-webkit-transform: rotate(1turn)
	}
}

.sign .reset-password-input {
	border-radius: 4px!important
}

.sign .return {
	margin-left: -8px;
	color: #969696
}

.sign .return:hover {
	color: #333
}

.sign .return i {
	margin-right: 5px
}

.sign .icheckbox_square-green {
	display: inline-block;
	*display: inline;
	vertical-align: middle;
	margin: 0;
	padding: 0;
	width: 18px;
	height: 18px;
	background: url(/static/image/green.png) no-repeat;
	border: none;
	cursor: pointer;
	background-position: 0 0
}

.sign .icheckbox_square-green.hover {
	background-position: -20px 0
}

.sign .icheckbox_square-green.checked {
	background-position: -40px 0
}

.sign .icheckbox_square-green.disabled {
	background-position: -60px 0;
	cursor: default
}

.sign .icheckbox_square-green.checked.disabled {
	background-position: -80px 0
}


.geetest_panel_box>* {
	box-sizing: content-box
}

@media (max-width:768px) {
	body {
		min-width: 0
	}

	.sign {
		height: auto;
		min-height: 0;
		background-color: transparent
	}

	.sign .logo {
		display: none
	}

	.sign .main {
		position: absolute;
		left: 50%;
		margin: 0 0 0 -200px;
		box-shadow: none
	}
}
</style>
