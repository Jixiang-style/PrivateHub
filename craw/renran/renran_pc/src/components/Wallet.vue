<template>

</template>

<script>
    export default {
        name: "Wallet",
        data(){
          return {
            token:"",
          }
        },
        created() {
          this.token = this.$settings.check_user_login(this);
          // 把支付宝的同步结果通知转发给服务端
          this.get_pay_result();
        },
        methods:{
          get_pay_result(){
            // 判断是否是从支付页面返回
            if(this.$route.query.out_trade_no){
              // 转发支付结果到服务端
              this.$axios.get(`${this.$settings.Host}/payments/alipay/result/`+location.search,{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{

              }).catch(error=>{
                this.$message.error("支付结果处理有误！请及时联系客服工作人员！");
              });
            }
          }
        }
    }
</script>

<style scoped>

</style>
