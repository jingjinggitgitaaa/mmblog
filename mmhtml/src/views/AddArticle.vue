<template>
    <div>
        <el-row :gutter="10">
            <el-col :xs="24" :lg="8">
                <div class="mm">
                    <el-form :label-position="'left'" label-width="80px" :model="article_info">
                        <el-form-item label="文章标题">
                        <el-input v-model="article_info.title"></el-input>
                        </el-form-item>
                        <el-form-item label="文章描述">
                        <el-input type='textarea' :rows="4" v-model="article_info.descript"></el-input>
                        </el-form-item>
                    </el-form>
                </div>

            </el-col>
            <el-col :xs="24" :lg="16">
                <div class="mm">
                    <div v-for=" (img,index) in cover_list" :key="index">
                        <el-image
                            v-if="img == cover_img"
                            class = "cover"
                            style="width: 200px; height: 150px"
                            :src="img"
                            :fit="'cover'"
                            @click="chooseCover(img)"></el-image>
                            <el-image
                            v-else
                            class = ""
                            style="width: 200px; height: 150px"
                            :src="img"
                            :fit="'cover'"
                            @click="chooseCover(img)"></el-image>
                    </div>
                    <el-button type="success" round @click="submitArticle()">保存文章</el-button>
                </div>

            </el-col>
            <el-col :xs="24" :lg="24">
                <div class="mm">
                    <div id='summernote'>
                    </div>
                </div>

            </el-col>
        </el-row>
    </div>
</template>
<script>
import $ from 'jquery'
import axios from 'axios'
import Qs from 'qs'
export default {
    data(){
        return{
            article_info:{
                title:'',
                descript:'',
                contents:''
            },
            cover_img:'',
            cover_list :[],
        }
    },
    methods: {
        submitArticle(){
            if (this.article_info.title.length == 0){
                alert('请填写文章标题')
                return
            }
            let article_data = {
                title:this.article_info.title,
                descript:this.article_info.descript,
                content:this.article_info.contents,
                cover:this.cover_img,
                token:this.$store.getters.isnotUserlogin
            }
            console.log(article_data)
            axios.post('http://127.0.0.1:9000/api/add-article/',Qs.stringify(article_data))
            .then(res=>{
                if(res.data == 'nologin'){
                    alert('用户登录已过期，请重新登录')
                    this.$router.push({path:'/login'})
                }
                if(res.data=='ok'){
                    window.location.reload()
                }
                console.log(res)
            })
            .catch(err=>{
                console.log(err)
            })
        },
        chooseCover(img){
            // console.log(img)
            this.cover_img = img
        },
        summernote(){
            let self = this
            $('#summernote').summernote({
                width:"100%",
                height:500,
                lang:'zh-C',
                callbacks:{
                    onChange(contents){
                        console.log(contents)
                        self.article_info.contents = contents
                    },
                    onImageUpload(files){
                        console.log(files)
                        let img = files[0] 
                        let imgData = new FileReader()
                        imgData.readAsDataURL(img)
                        imgData.onload = function(){
                            //插入图片本身
                            let imgnode = document.createElement('img')
                            imgnode.src = imgData.result
                            $('#summernote').summernote('insertNode',imgnode)

                            //推入封面
                            self.cover_list.push(imgData.result)
                        }
                        
                        
                    },
                    onImageLinkInsert(url){

                        let imgnode = document.createElement('img')
                        imgnode.src = url

                        $('#summernote').summernote('insertNode',imgnode)
                        self.cover_list.push(url)
                    },
                    onMediaDelete(target){
                        // console.log(target)
                        let imgData = target[0].src 
                        // console.log(imgData)
                        for (let i = 0; i < self.cover_list.length; i++) {
                            if(self.cover_list[i] == imgData){
                                self.cover_list.splice(i,1)
                            }
                            
                        }                    }
                }
            })
        }
    },
    mounted(){
        this.summernote()
    }
}
</script>
<style scoped>
.mm{
    min-height: 200px;
    padding:20px 20px;
    display: flex;
    align-content: center;
    justify-content: center;
}
.el-form-item{
    margin-top:22px;
}
.mm .el-button{
    position: fixed;
    right:20px;
    z-index: 1001;
    margin-top: 186px;
}
.mm .el-image.cover{
    border:2px solid #ffc815;
}
.mm .el-image:hover{
    border:2px solid #ffc815;
}
</style>