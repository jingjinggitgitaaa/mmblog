from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import datetime
from blog.models import Article,Userinfo
import base64
import os
import json


hostUrl = 'http://127.0.0.1:9000'

@api_view(['POST'])
def mm_login(request):
    username = request.POST['username']
    password = request.POST['password']
    token = ''
    #登录逻辑
    user = User.objects.filter(username=username)
    if user:
        checkPwd = check_password(password,user[0].password)
        if checkPwd:
            userinfo = Userinfo.objects.get(belong=user[0])
            token = Token.objects.get_or_create(user=user[0])
            token = Token.objects.get(user=user[0])
        else:
            return Response('pwderr')

    else:
        return Response('none')
    userinfo_data = {
        'token':token.key,
        'nickname':userinfo.nickName,
        'headImg':str(userinfo.headImg)
    }

    return Response(userinfo_data)

@api_view(['POST'])
def mm_register(request):
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    user = User.objects.filter(username=username)
    if user:
        return Response('repeat')
    else:
        newPwd = make_password(password,username)
        newUser = User(username=username,password=newPwd)
        newUser.save()
    token = Token.objects.get_or_create(user=newUser)
    token = Token.objects.get(user=newUser)
    userinfo = Userinfo.objects.get_or_create(belong=newUser)
    userinfo = Userinfo.objects.get(belong=newUser)
    userinfo_data = {
        'token':token.key,
        'nickname':userinfo.nickName,
        'headImg':str(userinfo.headImg)
    }

    return Response(userinfo_data)

@api_view(['POST'])
def auto_login(request):
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)

    if user_token:
        # print(user_token)
        userinfo = Userinfo.objects.get(belong=user_token[0].user)
        userinfo_data = {
            'token':token,
            'nickname':userinfo.nickName,
            'headImg':str(userinfo.headImg)
        }
        return Response(userinfo_data)
    else:
        return Response('tokenTimeout')


@api_view(['POST'])
def logout(request):
    token = request.POST['token']
    user_token = Token.objects.get(key=token)
    user_token.delete()
    return Response('logout')


@api_view(['POST'])
def add_article(request):
    title =request.POST['title']
    descript =request.POST['descript']
    content =request.POST['content']
    cover =request.POST['cover']
    token = request.POST['token']
    
    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')


    new_article = Article(title=title)
    new_article.save()
    # print(title)
    #解析富文本标签
    soup = BeautifulSoup(content,'html.parser')
    #获取所有html标签
    imgList = soup.find_all('img')
    # print(imgList)
    for i in range(0,len(imgList)):
        src = imgList[i]['src']
        
        #判断图片是远程图片还是本地图片
        if 'http://' in src or 'https://' in src:
            # print('link')
            image = requests.get(src)
            #请求远程图片
            #转化为二进制
            image_data = Image.open(BytesIO(image.content))
            # print(image_data)
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+str(new_article.id)+'-'+str(i)+'.png'
            image_data.save('upload/'+image_name)
            new_src = hostUrl + '/upload/'+image_name

            content = content.replace(src,new_src)

            #封面设定
            if cover == src:
                cover = new_src
        else:
            image_data = base64.b64decode(src.split(',')[1])
            pattern = src.split(',')[0].split('/')[1].split(';')[0]
            # print(pattern)
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+str(new_article.id)+'-'+str(i)+'.'+pattern
            # print(image_name)
            image_url = os.path.join('upload',image_name).replace('\\','/')
            with open(image_url,'wb') as f:
                f.write(image_data)
            new_src = hostUrl+'/' + image_url
            content = content.replace(src,new_src)

            #封面设定
            if cover == src:
                cover = new_src

    new_article.content = content
    new_article.cover = cover
    new_article.descript = descript
    new_article.belong = user_token[0].user
    new_article.save()
    return Response('ok')

    
@api_view(['GET'])
def articleList(request):
    page = request.GET['page']
    pageSize = request.GET['pageSize']
    article = Article.objects.all()
    #总条数
    total = len(article) 

    paginator = Paginator(article,pageSize)

    try:
        article = paginator.page(page)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = paginator.page(paginator.num_pages)

    article_data = []
    for a in article:
        a_item = {
            'title':a.title,
            'cover':a.cover,
            'nickname':'',
            'id':a.id
        }
        userinfo = Userinfo.objects.filter(belong=a.belong)
        if userinfo:
            a_item['nickname'] = userinfo[0].nickName
        else:
            a_item['nickname'] = a.belong.username
        article_data.append(a_item)

    return Response({'data':article_data,'total':total})

@api_view(['DELETE'])
def deleteArticle(request):
    id = request.POST['id']
    token = request.POST['token']
    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')

    article = Article.objects.filter(id=id)[0]
    article.delete()
    return Response('ok')


@api_view(['POST'])
def check_user_permission(request):

    token = request.POST['token']
    contentType = request.POST['contentType']
    permissions = json.loads(request.POST['permissions'])

    user_token = Token.objects.filter(key=token)
    if len(user_token)==0:
        return Response('nologin')
    
    user = user_token[0].user
    for p in permissions:
        perm_str = contentType+'.'+p
        # print(perm_str)
        check = user.has_perm(perm_str)
        # print(check)

        if check == False:
            return Response('noperm')

    return Response('ok')