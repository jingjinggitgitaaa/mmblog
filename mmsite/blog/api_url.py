from django.urls import path
from blog import api

urlpatterns = [
    path('add-article/', api.add_article),
    #用户管理
    #登录
    path('mm-login/',api.mm_login),
    #注册
    path('mm-register/',api.mm_register),
    path('auto-login/',api.auto_login),
    path('mm-logout/',api.logout),
    path('mm-articlelist/',api.articleList),
    path('mm-deleteArticle/',api.deleteArticle),
    path('mm-checkPerm/',api.check_user_permission)

]