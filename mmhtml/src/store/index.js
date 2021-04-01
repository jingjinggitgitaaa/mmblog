import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import Qs from 'qs'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userinfo:{}
  },
  getters:{
    isnotUserlogin(state){
      return state.userinfo.token
    }
  },
  mutations: {
    //保存注册登录用户信息
    saveUserinfo(state,userinfo){
      state.userinfo = userinfo
    },
    //清空用户登录状态
    clearUserinfo(state){
      state.userinfo = {}
    }
  },
  actions: {
    //登录
    blogLogin({commit},formData){
      axios({
        url:"http://127.0.0.1:9000/api/mm-login/",
        method:'post',
        data:Qs.stringify(formData)
      }).then((res)=>{
        if(res.data=='none'){
          alert('用户名不存在')
          return
        }
        if(res.data=='pwderr'){
          alert('密码错误')
          return
        }
        console.log(res.data)
        commit('saveUserinfo',res.data)
        localStorage.setItem('token',res.data.token)
        router.push({path:'/'})
      })
    },
    //注册
    blogRegister({commit},formData){
      axios({
        url:'http://127.0.0.1:9000/api/mm-register/',
        method:'post',
        data:Qs.stringify(this.formData)
      }).then((res)=>{
        console.log(res.data)
        if(res.data=='repeat'){
            alert('用户已存在')
        }
        commit('saveUserinfo',formData)
        localStorage.setItem('token',res.data.token)
        router.push({path:'/'})
      }).catch((err)=>{
        console.log(err)
      })
    },
    //自动登录
    tryAutoLogin({commit}){
      let token = localStorage.getItem('token')
      if(token){
        console.log('tryauto')
        console.log(token)
        axios({
          url:"http://127.0.0.1:9000/api/auto-login/",
          method:'post',
          data:Qs.stringify({token})
        }).then((res)=>{
          if(res.data == 'tokenTimeout'){
            alert('用户信息过期，请重新登录')
            router.push({path:'/login'})
          }else{
            // console.log(res.data)
            commit('saveUserinfo',res.data)
            localStorage.setItem('token',res.data.token)
            router.push({path:'/'})
          }
          
        })
        
      }
    },
    //退出登录
    blogLogout({commit}){
      let token = localStorage.getItem('token')
      commit('clearUserinfo')
      localStorage.removeItem('token')
      axios({
        url:"http://127.0.0.1:9000/api/mm-logout",
        method:'post',
        data:Qs.stringify({token})
      }).then((res)=>{
        console.log(res.data)
        
      })
      // router.push({path:'/'})

    },
    //检查用户权限
    checkPerm({getters},checkInfo){

      let token = getters.isnotUserlogin
      let permissions = checkInfo.permissions
      let contentType = checkInfo.contentType

      axios({
        url:"http://127.0.0.1:9000/api/mm-checkPerm/",
        method:"post",
        data:Qs.stringify({
          token,
          contentType,
          permissions:JSON.stringify(permissions)
        })
      }).then((res)=>{
        console.log(res.data)
        if(res.data=='nologin'){
          alert('用户登录已过期，请先登录')
          return
        }
        if(res.data == 'noperm'){
          alert('无权限，请联系管理员')
          router.push({path:'/'})
          return
        }
      })
    }
  },
  modules: {
  }
})
