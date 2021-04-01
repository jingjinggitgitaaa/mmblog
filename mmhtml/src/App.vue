<template>
  <!-- 头部导航 -->
  <div id="app">
    <div id="top-menu" class="mm">

    </div>
    <!-- 侧边左导航 -->
    <div id="left-menu" :class="'mm '+mobile_left">
      <i id="left-btn" @click="showHideLeftMenu" :class="fold"></i>
      <!-- 导航栏 -->
      <el-col :span="24" style="margin-top:60px">
        <el-menu
        class="el-menu-vertical-demo"
        background-color="#00000000"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
        @select='chooseMenu'>
        <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span>文章管理</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index='/add-article'>发布文章</el-menu-item>
          <el-menu-item index="/article-list" >文章列表</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-menu-item index="/user-permission">
        <i class="el-icon-user"></i>
        <span slot="title">用户管理</span>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-money"></i>
        <span slot="title">打赏记录</span>
      </el-menu-item>
      <el-menu-item index="4">
        <i class="el-icon-s-operation"></i>
        <span slot="title">栏目管理</span>
      </el-menu-item>
      <el-menu-item v-if="authUserLogin" @click="blogLogout()">
        <i class="el-icon-back"></i>
        <span slot="title">退出登录</span>
      </el-menu-item>
      </el-menu>
      </el-col>
    </div>
    <!-- 网页内容 -->
    <div id="content" :class='mobile_content'>
      <router-view :screenWidth="screenWidth"></router-view>
      <div id="footer" class="mm">
      <span>Copyright @曼曼怎么学习好呢工作室</span>
    </div>
    </div>
    
  </div>
</template>

<script>
  export default {
    data() {
      return {
        screenWidth:document.body.clientWidth,
        mobile_left:'',
        mobile_content:'',
        fold:"el-icon-s-unfold"
      }
    },
    watch:{
      //监听用户token
      authUserLogin(newVal){
        if(newVal==null){
          this.$router.push({path:'/login'})
        }
      },

    },
    computed:{
      //验证用户登录
      authUserLogin(){
        return this.$store.getters.isnotUserlogin
      }
    },
    created(){
      this.$store.dispatch('tryAutoLogin')
    },
    mounted(){
      // console.log(this.screenWidth)
      window.onresize = ()=>{
        this.screenWidth = document.body.clientWidth
        // console.log(this.screenWidth)
      }
      this.changeDevice()
    },
      methods: {
        changeDevice(){
          if(this.screenWidth <= 500){
            this.mobile_left = 'xs'
            this.mobile_content = 'xs'
          }
        },
        showHideLeftMenu(){
          // console.log(this.mobile)
          if(this.mobile_left == ''){
            this.mobile_left = 'xs'
            this.fold = "el-icon-s-unfold"
          }else{
            this.mobile_left = ''
            this.fold = "el-icon-s-fold"
          }
          //宽屏
          if(this.screenWidth > 500){
            if(this.mobile_content == ''){
              this.mobile_content = 'xs'
            }else{
              this.mobile_content = ''
            }
          }
        },
      chooseMenu(index){
        // console.log(index)
        this.$router.push({path:index})
      },
      //退出登录
      blogLogout(){
        this.$store.dispatch('blogLogout')
      }
      }
      

  };
</script>

<style>
.el-col{
  margin-top:5px;
}
</style>
