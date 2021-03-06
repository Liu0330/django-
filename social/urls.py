"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user import api as user_api
from swiper import api as swiper_api
urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'api/user/phone', user_api.user_phone),
    url(r'api/user/vcode', user_api.user_vcode),
    url(r'api/user/profile', user_api.user_profile),
    url(r'api/user/add', swiper_api.swiper_add),
    url(r'api/user/show', swiper_api.swiper_showusers),

    url(r'api/user/avatar', user_api.user_avatar),#添加一百人

    url(r'api/swiper/users', swiper_api.swiper_users),
    url(r'api/swiper/like', swiper_api.swiper_like),
    #    url(r'api/user/submit/vcode', user_api.submit_vcode),
]

