<template>
  <div class="write" v-show="is_show_page">
    <div class="_2v5v5">
      <div class="_3zibT"><a href="/">回首页</a></div>
      <div class="_1iZMb">
        <div class="_33Zlg" @click="collection_form=true"><i class="fa fa-plus"></i><span>新建文集</span></div>
        <div class="_2G97m">
          <form class="M8J6Q" :class="collection_form?'_2a1Rp':'_1mU5v'">
            <input type="text" placeholder="请输入文集名..." v-model="collection_name" class="_1CtV4">
            <button type="submit" class="dwU8Q _3zXcJ _3QfkW" @click.prevent.stop="add_collection"><span>提 交</span></button>
            <button type="button" class="vIzwB _3zXcJ" @click="collection_form=false"><span>取 消</span></button>
          </form>
        </div>
      </div>
      <ul class="_3MbJ4 _3t059">
        <li class="_3DM7w" :class="current_collection==key?'_31PCv':''" :title="collection.name" v-for="collection,key in collection_list" :key="key">
          <div class="_3P4JX _2VLy-" v-if="current_collection==key" @click.stop="show_collection_menu">
            <i class="fa fa-gear"></i>
            <span>
              <ul class="_2V8zt _3FcHm _2w9pn" :class="is_show_collection_menu?'NvfK4':''">
                <li class="_2po2r cRfUr" title="" @click.stop="edit_collection">
                  <span class=""><i class="fa fa-pencil-square-o _22XWG"></i>修改文集</span>
                </li>
                <li class="_2po2r cRfUr" title="">
                  <span class=""><i class="fa fa-trash-o _22XWG"></i>删除文集</span>
                </li>
              </ul>
            </span>
          </div>
          <span @click="current_collection=key">{{collection.name}}</span>
        </li>
      </ul>
      <div style="height: 50px;"></div>
      <div role="button" class="h-5Am">
        <span class="ant-dropdown-trigger"><i class="fa fa-bars"></i><span>设置</span></span>
        <span class="Yv5Zx">遇到问题<i class="fa fa-question-circle-o"></i></span>
      </div>
    </div>
    <div class="rQQG7">
      <div class="_3revO _2mnPN">
        <div class="_3br9T">
          <div>
            <div class="_1GsW5" @click.stop="add_article(0)"><i class="fa fa-plus-circle"></i><span> 新建文章</span></div>
            <ul class="_2TxA-">
              <li class="_25Ilv" @click.stop="current_article=key" :class="current_article==key?'_33nt7':''" :title="article.name" v-for="article,key in article_list" :key="key">
                <i class="_13kgp" :class="article.is_public?'_2m93u':''"></i>
                <div class="_3P4JX poOXI" v-if="current_article==key" @click.stop="show_article_menu">
                  <i class="fa fa-gear"></i>
                  <span>
                    <ul class="_2V8zt _3FcHm _2w9pn" :class="is_show_article_menu?'NvfK4':''">
                      <li class="_2po2r cRfUr" title="" v-if="!article.is_public" @click.stop="public_article(true)"><span class=""><i class="fa fa-share _22XWG"></i>直接发布</span></li>
                      <li class="_2po2r cRfUr" title="" v-else @click.stop="public_article(false)"><span class=""><i class="fa fa-lock _22XWG"></i>设为私密</span></li>
                      <li class="_2po2r cRfUr" title="" @click.stop="is_interval_pub_article=true;is_show_article_menu=false;"><span class=""><i class="fa fa-clock-o _22XWG"></i>定时发布</span></li>
                      <li class="_2po2r cRfUr" title=""><span class="_20tIi"><i class="iconfont ic-paid _22XWG"></i>发布为付费文章</span></li>
<!--                      <li class="_2po2r cRfUr" title=""><span class=""><i class="iconfont ic-set _22XWG"></i>设置发布样式</span></li>-->
                      <li class="_3nZXj _2_WAp _3df2u _2po2r cRfUr" title=""><span class=""><i class="fa fa-folder-open _22XWG"></i>移动文章
                        <div class="_3x4X_">
                          <ul class="_2KzJx oGKRI _3DXDE _2w9pn">
                            <li class="_2po2r cRfUr" :title="collection.name" v-for="collection in collection_list" v-if="collection.id!=article.collection" @click.stop="move_article(collection.id)"><span class="">{{collection.name}}</span></li>
                          </ul>
                        </div>
                      </span>
                      </li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-history _22XWG"></i>历史版本</span></li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-trash-o _22XWG"></i>删除文章</span></li>
                      <li class="_2po2r cRfUr" title=""><span class=""><i class="fa fa-ban _22XWG"></i>设置禁止转载</span></li>
                    </ul>
                  </span>
                </div>
                <span class="NariC">{{article.name}}</span>
                <span class="hLzJv" v-show="current_article==key">{{article.content}}</span>
                <span class="_29C-V" v-show="current_article==key">字数:{{article.content?article.content.length:0}}</span>
              </li>
            </ul>
            <div class="_2cVn3" @click.stop="add_article(1)"><i class="fa fa-plus"></i><span> 在下方新建文章</span></div>
          </div>
        </div>
      </div>
      <input type="text" class="_24i7u" v-model="editorTitle" v-if="article_list.length>0">
      <div id="editor" v-if="article_list.length > 0">
        <mavon-editor
          style="height: 100%"
          v-model="editorContent"
          @change="change_article"
          :ishljs="true"
          ref=md
          @imgAdd="imgAdd"
          @imgDel="imgDel"
        ></mavon-editor>
      </div>
    </div>
    <!-- 定时发布弹窗 -->
    <div class="interval_box" v-show="is_interval_pub_article">
      <transition name="el-fade-in-linear">
        <div class="transition-box">
          <div class="_2tIvb">
            <div class="ZTNas" @click.stop="is_interval_pub_article=false;"><i class="fa fa-close"></i></div>
            <div class="_1KgC3">
              <div class="-K8Re">定时发文 </div>
            </div>
            <div class="_1LROK PWCkH">
              <div class="wzwGh">选择定时发文的时间：</div>
              <div class="On4jq">
                  <el-date-picker
                  v-model="pub_date"
                  type="datetime"
                  format="yyyy-MM-dd HH:mm"
                  placeholder="选择日期时间">
                </el-date-picker>
              </div>
              <div class="_3mEYS">本文章将于<span class="yfqan">{{timeformat(pub_date)}}</span>发布。
              </div>
            </div>
            <div class="RzhZ5 pCffa">
              <button type="button" class="_3zXcJ" @click.stop="is_interval_pub_article=false;"><span>取 消</span></button>
              <button type="button" class="_3zXcJ _3QfkW" @click.stop="interval_pub_article"><span>确 认</span></button>
            </div>
          </div>

        </div>
      </transition>
    </div>

  </div>
</template>
<script>
    import { mavonEditor } from 'mavon-editor'
    import 'mavon-editor/dist/css/index.css';
    import "../../static/font-awesome/css/font-awesome.css";
    export default {
        name: "Write",
        data(){
            return {
                is_show_page: false,
                img_file:[],            // 记录当前编辑中用户上传的图片集合
                collection_form:false,
                token: "",
                collection_list:[],     // 当前用户的文集列表
                current_collection: 0,  // 默认让用户选中的文集的下标为0
                collection_name: "",    // 新建文集表单中的文集名称
                is_show_collection_menu: false,    // 是否显示文集菜单
                article_list: [],
                current_article: 0,     // 默认让用户选中的文章的下标为0
                is_show_article_menu: false,    // 是否显示文章菜单
                pub_date: new Date().toLocaleDateString(),  // 定时发布文章的事件设置
                is_interval_pub_article: false,
                editorTitle:"",   // 当前编辑文章的标题
                editorContent:"", // 当前编辑文章的内容
                editorContentRender:"", // 当前编辑文章的内容[解析后的html代码]
                timer:"",  // 提供给文章编辑的定时器使用的变量,用于保存定时器的返回值
            }
        },
        watch:{
            current_collection(){
                this.get_article_list();
                // 填充当前编辑的文章标题和内容
                if(this.article_list[this.current_article]){
                  this.editorTitle = this.article_list[this.current_article].name;
                  if(this.article_list[this.current_article].content){
                      this.editorContent = this.article_list[this.current_article].content
                  }else{
                      this.editorContent = "";
                  }
                }
            },
            current_article(){
                // 填充当前编辑的文章标题和内容
                if(this.article_list[this.current_article]){
                  this.editorTitle = this.article_list[this.current_article].name;
                  if(this.article_list[this.current_article].content){
                      this.editorContent = this.article_list[this.current_article].content
                  }else{
                      this.editorContent = "";
                  }
                }
            },
            editorTitle(){
                this.save_article();
            }
        },
        created(){
          this.token = this.$settings.check_user_login(this);
          if(this.token){
              // 显示页面
              this.is_show_page = true;
              // 获取文集
              this.get_collection();
          }
        },
        mounted(){
            if(this.article_list.length>0){
              document.querySelector("#editor").style.height = document.documentElement.clientHeight-document.querySelector("._24i7u").clientHeight+"px";
            }
            // 给当前网页绑定点击事件
            document.onclick = ()=>{
                // 点击文档,隐藏操作文集的的菜单
                this.hide_collection_menu();
                this.hide_article_menu();
            }
        },
        components: {
          mavonEditor
        },
        methods:{
          // 绑定@imgAdd event
          imgAdd(filename, $fileobj){
              // 添加文件
              // 第一步.将图片上传到服务器.
              var formdata = new FormData();
              formdata.append('image', $fileobj);
              this.img_file[filename] = $fileobj;
              this.$axios.post(`${this.$settings.Host}/article/image/`,formdata,{
                  headers:{
                      'Content-Type': 'multipart/form-data',
                      "Authorization": "jwt " + this.token,
                  }
              }).then(response=>{
                  // 将返回的url替换到文本原位置![...](0) -> ![...](url)
                  this.$refs.md.$img2Url(filename, response.data.image);
              });
          },
          imgDel(filename) {
              // 删除文件
              delete this.img_file[filename];  // 前段删除,一般服务端不删除
              this.$refs.toolbar_left.$imgDelByFilename(filename);
          },
          get_collection(){
              // 获取当前登陆用户的文集
              this.$axios.get(`${this.$settings.Host}/article/collection/`,{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  this.collection_list = response.data;
                  // 获取当前文集下的所有文章
                  this.get_article_list();
              }).catch(error=>{
                  this.$message.error("对不起,无法获取当前用户的文集列表!");
              });
          },
          add_collection(){
              // 添加文集
              if(this.collection_name.length<1){
                  // 不能为空!
                  this.$message.error("对不起,文集名称不能为空!");
                  return;
              }

              // 发送ajax
              this.$axios.post(`${this.$settings.Host}/article/collect/`,{
                  name: this.collection_name
              },{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  this.$message.success("添加文集成功!");
                  this.collection_name = "";
                  this.collection_form = false; // 隐藏添加文集的表单
                  // 把服务端中添加返回的文集信息,保存到collection_list中
                  this.collection_list.unshift(response.data);
                  this.current_collection = 1;
                  this.current_collection = 0;
              }).catch(error=>{
                  this.$message.error(error.response.data);
              })

          },
          show_collection_menu(){
              // 控制当前文集菜单的显示隐藏
              this.is_show_collection_menu = !this.is_show_collection_menu;
          },
          hide_collection_menu(){
              // 隐藏操作文集的菜单
              this.is_show_collection_menu = false;
          },
          edit_collection(){
              // 修改文集
              this.$prompt('请输入新文集名', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputPattern: /.{1,}/,
                inputErrorMessage: '文集名称不能为空!'
              }).then(({ value }) => {
                 // 点击确定,需要把当前文集名称提交到服务端进行修改
                 let collection_id = this.collection_list[this.current_collection].id;
                 this.$axios.put(`${this.$settings.Host}/article/collect/${collection_id}/`,{
                     name: value,
                 },{
                     headers:{
                         Authorization:"jwt " + this.token,
                     }
                 }).then(response=>{
                     this.collection_list[this.current_collection].name = value;
                 }).catch(error=>{
                     this.$message.error(error.response.data);
                 })
              }).catch(() => {

              });
          },
          del_collection(){
              // 删除文集
              // 获取当前文件的id
              let collection_id = this.collection_list[this.current_collection].id;
              // 刚发送ajax

          },
          get_article_list(){
              // 获取文章列表
              this.$axios.get(`${this.$settings.Host}/article/`,{
                  params:{
                      collection: this.collection_list[this.current_collection].id,
                  },
                  headers:{
                     Authorization:"jwt " + this.token,
                  }
              }).then(response=>{
                  this.article_list = response.data;
                  // 填充当前编辑的文章标题和内容
                  if(this.article_list[this.current_article]){
                    this.editorTitle = this.article_list[this.current_article].name;
                    if(this.article_list[this.current_article].content){
                        this.editorContent = this.article_list[this.current_article].content
                    }else{
                        this.editorContent = "";
                    }
                  }
              }).catch(error=>{
                  this.$message.error(error.response.data);
              })
          },
          show_article_menu(){
              // 控制当前文章菜单的显示隐藏
             this.is_show_article_menu = !this.is_show_article_menu;
          },
          hide_article_menu(){
             this.is_show_article_menu = false;
          },
          add_article(position){ // position 表示添加文章位置
              // 在前面添加文章
              this.$axios.post(`${this.$settings.Host}/article/`,{
                  position: position,
                  collection: this.collection_list[this.current_collection].id,
              },{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  if(position==0){
                      // 把文章设置为前面位置
                      this.article_list.unshift(response.data);
                  }else {
                      // 把文章设置为后面位置
                      this.article_list.push(response.data);
                  }
              }).catch(error=>{
                  this.$message.error(error.response.data);
              })
          },
          public_article(is_public){
              // 文章发布状态的切换
              let article_id = this.article_list[this.current_article].id;
              this.$axios.put(`${this.$settings.Host}/article/public/${article_id}/`,{
                  is_public: is_public,
              },{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  this.article_list[this.current_article].is_public=is_public;
                  this.is_show_article_menu = false;
                  if(is_public){
                      // 对页面进行跳转到文章发布投稿页面
                      sessionStorage.current_article_id = this.article_list[this.current_article].id;
                      sessionStorage.current_article_name=this.article_list[this.current_article].name;
                      this.$router.push("/post");
                  }else{
                      this.$message.success("文章设置成功!");
                  }

              }).catch(error=>{
                  this.$message.error("操作失败!请联系客服工作人员!");
              })
          },
          move_article(collection_id){
              // 文章发布状态的切换
              let article_id = this.article_list[this.current_article].id;
              this.$axios.put(`${this.$settings.Host}/article/move/${article_id}/`,{
                  collection_id: collection_id,
              },{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  this.article_list.splice(this.current_article,1);
                  this.is_show_article_menu = false;
                  this.$message.success("文章设置成功!");

              }).catch(error=>{
                  this.$message.error("操作失败!请联系客服工作人员!");
              });
          },
          interval_pub_article(){
              // 定时发布文章
              let article_id = this.article_list[this.current_article].id;
              this.$axios.put(`${this.$settings.Host}/article/interval/${article_id}/`,{
                  pub_date: this.pub_date,
              },{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  this.article_list[this.current_article].is_public = true;
                  this.is_show_article_menu = false;
                  this.$message.success("文章设置成功!");
                  this.is_interval_pub_article = false;
              }).catch(error=>{
                  this.is_interval_pub_article = false;
                  this.$message.error("操作失败!请联系客服工作人员!");
              });
          },
          timeformat(time){
              time = new Date(time);
              return `${time.getFullYear()}-${time.getMonth()+1}-${time.getDate()} ${time.getHours()}:${time.getMinutes()}`;
          },
          change_article(value, render){
              // 监听编辑器内容发生改变
              this.editorContentRender = render;
              this.editorContent = value;
              this.save_article();
          },
          save_article(){
              // 保存文章
              clearTimeout(this.timer);
              this.timer = setTimeout(this.save_article_ajax,2000);
          },
          save_article_ajax(){
              // 保存文章的请求代码
              let article_id = this.article_list[this.current_article].id;
              this.$axios.put(`${this.$settings.Host}/article/save/${article_id}/`,{
                  name: this.editorTitle,
                  content: this.editorContent,
                  render: this.editorContentRender,
              },{
                  headers:{
                      Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                  // this.$message.success("保存成功!");
              }).catch(error=>{
                  this.$message.error("保存失败!");
              });
          }
        }
    }
</script>

<style scoped>
  body *{
    box-sizing: border-box;
  }
  .write{
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    margin: 0;
  }
  ._2v5v5 {
    position: relative;
    height: 100%;
    overflow-y: auto;
    background-color: #404040;
    color: #f2f2f2;
    z-index: 100;
    width: 13.66666667%;
    display: block;
    flex: 0 0 auto;
    float: left;
    padding-right: 0;
    padding-left: 0;
    min-height: 1px;
  }
  ._3zibT {
    padding: 30px 18px 5px;
    text-align: center;
    font-size: 14px;
  }
  ._3zibT a {
    display: block;
    font-size: 15px;
    padding: 9px 0;
    color: #ec7259;
    border: 1px solid rgba(236,114,89,.8);
    border-radius: 20px;
    -webkit-transition: border-color .2s ease-in;
    -o-transition: border-color .2s ease-in;
    transition: border-color .2s ease-in;
  }
  ._1iZMb {
    padding: 0 15px;
    margin-top: 20px;
    margin-bottom: 10px;
    font-size: 14px;
    line-height: 1.5;
  }
  ._1iZMb ._33Zlg {
    cursor: pointer;
    color: #f2f2f2;
    transition: color .2s cubic-bezier(.645,.045,.355,1);
    font-size: 14px;
  }
  ._1iZMb ._33Zlg .fa+span {
    margin-left: 4px;
  }
  ._1iZMb ._2G97m {
    overflow: hidden;
  }
  ._1iZMb ._2a1Rp {
    height: 85px;
    opacity: 1;
    margin-top: 10px;
    transition: all .2s ease-out;
    overflow: hidden;
  }
  ._1CtV4 {
    width: 100%;
    height: 35px;
    color: #ccc;
    background-color: #595959;
    border: 1px solid #333;
    padding: 4px 6px;
    font-size: 14px;
    line-height: 20px;
    outline: 0;
    overflow: visible;
    margin: 10px 0 0;
    margin-bottom: 10px;
  }
._3zXcJ {
    position: relative;
    display: inline-block;
    text-align: center;
    height: 30px;
    line-height: 20px;
    padding: 4px 12px;
    border: 1px solid transparent;
    border-radius: 15px;
    font-size: 14px;
    font-weight: 500;
    -ms-touch-action: manipulation;
    touch-action: manipulation;
    cursor: pointer;
    background-image: none;
    white-space: nowrap;
    user-select: none;
    transition: all .2s cubic-bezier(.645,.045,.355,1);
    text-transform: none;
    color: #42c02e;
    border-color: #42c02e;
    margin-left: 4px;
    background-color: #404040;
  }
  .vIzwB {
    color: #999;
    outline: 0;
  }
  ._1iZMb ._1mU5v {
    height: 0;
    opacity: 0;
    margin-top: 0;
  }
  ._1iZMb ._2a1Rp {
    height: 85px;
    opacity: 1;
    margin-top: 10px;
  }
  ._1iZMb ._1mU5v, ._1iZMb ._2a1Rp {
    transition: all .2s ease-out;
  }
  .vIzwB, .vIzwB:focus, .vIzwB:hover {
    background-color: #404040;
    border-color: transparent;
  }
  .dwU8Q {
      margin-left: 4px;
      background-color: #404040;
  }
._3t059 {
    position: relative;
    z-index: 0;
    background-color: #8c8c8c;
}
._3MbJ4 {
    margin-bottom: 0;
}
._3DM7w {
    position: relative;
    line-height: 40px;
    list-style: none;
    font-size: 15px;
    color: #f2f2f2;
    background-color: #404040;
    padding: 0 15px;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
._31PCv {
    background-color: #666;
    border-left: 3px solid #ec7259;
    padding-left: 12px;

}
._3DM7w ._2VLy- {
    float: right;
}
._3P4JX {
    font-size: 16px;
    width: 40px;
    text-align: center;
    position: relative;
    min-height: 30px;
    max-height: 50px;
}
._3DM7w span {
    display: block;
    margin-right: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
._2w9pn {
    font-size: 14px;
    -webkit-box-shadow: 0 5px 10px rgba(0,0,0,.2);
    box-shadow: 0 5px 10px rgba(0,0,0,.2);
    list-style: none;
    background-color: #fff;
    color: #595959;
    border-radius: 6px;
}
._3P4JX ul._2V8zt {
    display: none;
    position: absolute;
    z-index: 99;
    right: 0;
}
._3P4JX ul._3FcHm {
    top: 100%;
}
._2po2r {
    padding: 10px 20px;
    line-height: 20px;
    white-space: nowrap;
    text-align: left;
    position: relative;
    border-bottom: 1px solid #d9d9d9;
}
._3DM7w:hover, .JUBSP {
    background-color: #666;
}
.h-5Am {
    display: block;
    width: 13.66666667%;
    position: fixed;
    bottom: 0;
    height: 50px;
    line-height: 50px;
    font-size: 15px;
    padding-left: 15px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    z-index: 150;
    background-color: #404040;
}
.cRfUr {
    border-bottom: 1px solid #d9d9d9;
}

._2_WAp ._2KzJx, ._2_WAp ._3x4X_ {
    position: absolute;
    right: 100%;
    top: 0;
    display: none;
    z-index: 10;
}
._2_WAp:hover ._2KzJx, ._2_WAp:hover ._3x4X_ {
    display: block;
}
._2po2r:last-child {
    border-radius: 0 0 4px 4px;
    border-bottom: 0;
}
._2po2r:first-child {
    border-radius: 4px 4px 0 0;
}
._2po2r ._22XWG {
    margin-right: 5px;
}
._2po2r:hover {
    background-color: #666;
    color: #fff;
}
._3DM7w span {
    display: block;
    margin-right: 20px;
    overflow: hidden;
    -o-text-overflow: ellipsis;
    text-overflow: ellipsis;
    white-space: nowrap;
}
._3P4JX ul.NvfK4 {
    display: block;
}
._3P4JX ul._2V8zt:before {
    position: absolute;
    right: 12px;
    content: "";
    display: inline-block;
}
._3P4JX ul._3FcHm:before {
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    border-bottom: 9px solid #fff;
    top: -9px;
}
.h-5Am .ant-dropdown-trigger {
    display: inline-block;
    color: #999;
    cursor: pointer;
    -webkit-transition: color .2s cubic-bezier(.645,.045,.355,1);
    -o-transition: color .2s cubic-bezier(.645,.045,.355,1);
    transition: color .2s cubic-bezier(.645,.045,.355,1);
}
.h-5Am .fa+span {
    margin-left: 4px;
}
.h-5Am .Yv5Zx {
    float: right;
    margin-right: 15px;
    color: #999;
    cursor: pointer;
  }
  .h-5Am .Yv5Zx i {
      margin-left: 5px;
  }
  .rQQG7{
    height: 100%;
    display: block;
    width: 33.33333%;
    border-right: 1px solid #d9d9d9;
  }
  ._3revO {
    overflow-y: scroll;
    height: 100%;
    position: relative;
  }
  ._3br9T {
    position: relative;
    transition: opacity .3s cubic-bezier(.645,.045,.355,1);
    opacity: 1;
  }
  ._1GsW5 {
    line-height: 20px;
    font-size: 15px;
    font-weight: 400;
    padding: 20px 0 20px 25px;
    cursor: pointer;
    color: #595959;
  }
  ._1GsW5:hover {
    color: #262626;
  }
  ._2TxA- {
    position: relative;
    margin-bottom: 0;
    background-color: #efe9d9;
    border-top: 1px solid #d9d9d9;
  }
  ._25Ilv {
    position: relative;
    height: 90px;
    color: #595959;
    background-color: #fff;
    margin-bottom: 0;
    padding: 15px 10px 15px 60px;
    box-shadow: 0 0 0 1px #d9d9d9;
    border-left: 5px solid transparent;
    list-style: none;
    line-height: 60px;
    cursor: pointer;
    user-select: none;
  }
  ._25Ilv ._2m93u {
    background: url(/static/image/sprite.9d24217.png) no-repeat -50px -25px;
    background-size: 250px;
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
  }
  ._1tqbw, ._25Ilv:hover, ._33nt7 {
    background-color: #e6e6e6;
  }
  ._25Ilv ._2m93u {
    background: url(/static/image/sprite.9d24217.png) no-repeat -50px -25px;
    background-size: 250px;
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
  }
  ._3P4JX {
    font-size: 16px;
    width: 40px;
    text-align: center;
    position: relative;
    min-height: 30px;
    max-height: 50px;
}
  ._25Ilv .poOXI {
    float: right;
}
  ._33nt7 {
    border-left-color: #ec7259;
  }
  ._25Ilv .hLzJv, ._25Ilv .NariC {
    display: block;
    height: 30px;
    line-height: 30px;
    margin-right: 40px;
    overflow: hidden;
    -o-text-overflow: ellipsis;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 18px;
    font-family: sans-serif;
}
  ._2TxA- {
    position: relative;
    margin-bottom: 0;
    background-color: #efe9d9;
    border-top: 1px solid #d9d9d9;
}
  ._3P4JX ul._2V8zt {
    display: none;
    position: absolute;
    z-index: 99;
    right: 0;
}
  ._3P4JX ul._3FcHm {
    top: 100%;
}
  ._2w9pn {
    font-size: 14px;
    box-shadow: 0 5px 10px rgba(0,0,0,.2);
    list-style: none;
    background-color: #fff;
    color: #595959;
    border-radius: 6px;
}
  ._3P4JX ul.NvfK4 {
    display: block;
}
  ._3P4JX ul._3FcHm:before {
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    border-bottom: 9px solid #fff;
    top: -9px;
}
  ._3P4JX ul._2V8zt:before {
    position: absolute;
    right: 12px;
    content: "";
    display: inline-block;
}
._25Ilv ._13kgp {
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
    background: url(/static/image/sprite.9d24217.png) no-repeat 0 -25px;
    background-size: 250px;
}
._25Ilv ._13kgp {
    position: absolute;
    top: 30px;
    left: 20px;
    width: 22px;
    height: 30px;
    background: url(/static/image/sprite.9d24217.png) no-repeat 0 -25px;
    background-size: 250px;
}
._25Ilv ._2m93u {
    background: url(/static/image/sprite.9d24217.png) no-repeat -50px -25px;
    background-size: 250px;
}
._25Ilv ._29C-V {
    position: absolute;
    bottom: 2px;
    left: 5px;
    font-size: 9px;
    line-height: 16px;
    color: #595959;
}
._2cVn3 {
    line-height: 30px;
    padding: 20px 0 20px 25px;
    cursor: pointer;
    color: #999;
    margin-bottom: 80px;
}
._24i7u {
    flex-shrink: 0;
    padding: 0 80px 10px 40px;
    margin-bottom: 0;
    border: none;
    font-size: 30px;
    font-weight: 400;
    line-height: 30px;
    box-shadow: none;
    color: #595959;
    background-color: transparent;
    outline: none;
    border-radius: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    position: absolute;
    top: 0;
    right: 0;
    width: 66.666666%;
}
  #editor {
    margin: auto;
    width: 66.666666%;
    position: absolute;
    right: 0;
    top: 44px;
    height: 580px;
  }
  /* 定时发布文章的相关样式 */

    .interval_box{
      display: flex;
      height: 280px;
      width: 400px;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      margin: auto;
      background: #fff;
      border-radius: 4px;
      z-index: 2000;
    }
    .NVdZF{display:block}

  ._20JYe {
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    background-color: hsla(0, 0%, 100%, .7);
    height: 100%;
    z-index: 1000;
    filter: alpha(opacity=30)
  }

  body.reader-night-mode ._20JYe {
    background-color: hsla(0, 0%, 40%, .7)
  }

  ._3WS2u {
    display: none
  }

  ._23VW8 {
    position: fixed;
    overflow: auto;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1010;
    -webkit-overflow-scrolling: touch;
    outline: 0
  }

  ._3cgNz {
    position: relative;
    background-color: #fff;
    width: auto;
    border: 0;
    border-radius: 6px;
    margin: 0 auto 24px;
    background-clip: padding-box;
    -webkit-box-shadow: 0 2px 8px rgba(0, 0, 0, .2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, .2)
  }

  body.reader-night-mode ._3cgNz {
    background-color: #3d3d3d
  }

  .cjahm {
    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%)
  }

  .cjahm.move-up-appear.move-up-appear-active, .cjahm.move-up-enter.move-up-enter-active {
    -webkit-animation-name: _2oyZp;
    animation-name: _2oyZp
  }

  .cjahm.move-up-leave.move-up-leave-active {
    -webkit-animation-name: _3g8pf;
    animation-name: _3g8pf
  }

  ._2tIvb {
    position: relative;
    border-radius: 6px;
    background-color: #eee;
  }

  body.reader-night-mode ._2tIvb {
    background-color: #3d3d3d
  }

  .ZTNas {
    position: absolute;
    right: 0;
    top: 0;
    width: 48px;
    height: 48px;
    line-height: 46px;
    text-align: center;
    font-size: 16px;
    cursor: pointer;
    color: #999;
    -webkit-transition: color .3s ease;
    -o-transition: color .3s ease;
    transition: color .3s ease
  }

  .ZTNas:hover {
    color: #4d4d4d
  }

  ._1KgC3 {
    padding: 13px 16px;
    border-radius: 4px 4px 0 0;
    color: #595959;
    border-bottom: 1px solid #d9d9d9
  }

  body.reader-night-mode ._1KgC3 {
    border-color: #2e2e2e
  }

  .-K8Re {
    margin: 0;
    font-size: 16px;
    line-height: 21px;
    font-weight: 500;
    color: #4d4d4d
  }

  body.reader-night-mode .-K8Re {
    color: #b3b3b3
  }

  ._3O4M2 {
    font-size: 13px;
    padding-left: 10px;
    color: #999
  }

  ._3O4M2 a {
    color: #3294d0
  }

  .PWCkH {
    padding: 16px;
    font-size: 12px;
    line-height: 1.5;
    color: #595959
  }

  body.reader-night-mode .PWCkH {
    color: #b3b3b3
  }

  .pCffa {
    padding: 0 16px 16px;
    text-align: right;
    border-radius: 0 0 2px 2px
  }

  ._26mjB {
    display: block
  }

  .HhIYk {
    zoom: 1
  }

  .HhIYk:after, .HhIYk:before {
    content: " ";
    display: table
  }

  .HhIYk:after {
    clear: both;
    visibility: hidden;
    font-size: 0;
    height: 0
  }

  ._37SYn {
    font-size: 13px;
    line-height: 20px;
    padding: 30px 30px 20px;
    color: #333
  }

  body.reader-night-mode ._37SYn {
    color: #b3b3b3
  }

  ._2BmdS {
    padding: 0 16px 16px;
    text-align: right;
    border-radius: 0 0 2px 2px
  }

  ._26mjB .PWCkH {
    padding: 0;
    border-radius: 2px
  }

  ._26mjB .PWCkH a {
    color: #3194d0
  }

  ._26mjB .PWCkH a:active, ._26mjB .PWCkH a:hover {
    color: #2b86bc
  }

  ._26mjB ._38pIX {
    padding: 30px 16px;
    border: 0
  }

  ._26mjB ._38pIX input {
    display: block;
    border-radius: 4px;
    width: 100%;
    line-height: 20px;
    padding: 5px 10px;
    font-size: 15px;
    background-color: transparent;
    border: 1px solid #ccc
  }

  body.reader-night-mode ._26mjB ._38pIX input {
    border-color: #2e2e2e
  }

  ._26mjB .ZTNas {
    width: 32px;
    height: 32px;
    line-height: 32px
  }

  .HSpeJ .PWCkH {
    border: 0
  }
</style>
