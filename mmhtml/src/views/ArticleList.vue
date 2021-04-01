<template>
<div id='article-list'>
    <div class='mm'>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>文章列表</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
    <div class='mm' style="margin-top:10px;">
        <el-row>
            <el-col :span='24' v-for="article in article_list" :key="article.id">
                <div class="card mm">
                    <el-row>
                        <el-col :xs='24' :lg='4'>
                            <el-image
                                v-if="screenWidth>500"
                                style="height: 100px;width:150px;"
                                :src="article.cover"
                                :fit="'cover'"></el-image>
                            <el-image
                                v-else
                                style="width:100%"
                                :src="article.cover"
                                :fit="'cover'"></el-image>
                        </el-col>
                        <el-col class="text-item" :xs='24' :lg='9'>
                            <span>{{article.title}}</span>
                        </el-col>
                        <el-col class="text-item" :xs='12' :lg='7'>
                            <span>发布者：{{article.nickname}}</span>
                        </el-col>
                        <el-col class="text-item" :xs='12' :lg='4'>
                            <el-button type="success" icon="el-icon-search" circle></el-button>
                            <el-button type="danger" icon="el-icon-delete" circle @click="deleteArticle(article.id,article.nickname)"></el-button>
                        </el-col>
                    </el-row>
                </div>
            </el-col>
        </el-row>
    </div>
    <!-- 分页器 -->
    <div class='mm' style="margin-top:10px;">
        <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="pageSize"
            @current-change="currentChange">
            </el-pagination>
    </div>
</div>
    
</template>
<script>
import axios from 'axios'
import Qs from 'qs'
export default {
    props:['screenWidth'],
    data(){
        return{
            total:100,
            pageSize:6,
            currentPage:1,
            article_list:[]
        }
    },
    mounted(){
        this.getArticleList(this.currentPage)
    },
    methods:{
        currentChange(val){
            console.log(val)
            this.currentPage = val
            this.getArticleList(this.currentPage)
        },
        getArticleList(page){
            console.log('getArticleList')
            console.log(page)
            axios({
                url:"http://127.0.0.1:9000/api/mm-articlelist/",
                method:'get',
                params:{
                    page,
                    pageSize:this.pageSize
                }
            }).then((res)=>{
                console.log(res)
                this.total = res.data.total
                this.article_list = res.data.data
            })
        },
        deleteArticle(id,nickname){
            if(nickname != this.$store.state.userinfo.nickname){
                alert('不能删除其他作者的文章')
                return
            }
            if(confirm('是否确定删除')){
                axios({
                url:"http://127.0.0.1:9000/api/mm-deleteArticle/",
                method:'delete',
                data:Qs.stringify({
                    id,
                    token:this.$store.getters.isnotUserlogin
                }),
                headers:{
                    "Content-Type":"application/x-www-form-urlencoded"
                }
            }).then((res)=>{
                console.log(res)
                if(res.data=='nologin'){
                    alert('用户登录过期，请先登录')
                    return
                }
                this.getArticleList(this.currentPage)
            })
            }
            
        }
    }
}

</script>
<style scoped>
#article-list .mm{
    padding:10px 10px;
    background-color: #00000060;
}
.card.mm .text-item{
    
    color:#fff;
    height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
    
}

</style>