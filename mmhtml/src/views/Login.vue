<template>
    <div id='login-page'>
        <div class='mm loginbox'>
            <div class='header'>
                用户登录
                <el-divider></el-divider>
            </div>
            <el-form :label-position="'right'" label-width="60px" :model="formData">
                <el-form-item label="用户名">
                    <el-input v-model="formData.username"></el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="formData.password"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="success" round @click="blogLogin()">登录</el-button>
                    <el-button type="warning" round @click="toRegister()">前往注册</el-button>
                </el-form-item>
                
            </el-form>
        </div>
    </div>
</template>

<script>

export default {
    data(){
        return{
            formData:{
                username:'',
                password:'',
            }
        }
    },
    methods:{
        toRegister(){
            this.$router.push({path:'/register'})
        },
        blogLogin(){
            if(this.formData.username.length==0 || this.formData.password.length==0){
                alert('表单填写完整')
                return
            }
            this.$store.dispatch('blogLogin',this.formData)
        }
    }
}
</script>

<style scoped>
#login-page{
    height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.loginbox{
    padding:10px 10px;

}
</style>