
from django.conf.urls import url

from apps.users import views

urlpatterns = [
    # 1.注册页面 显示
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    # 2. 判断用户名是否重复 usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),

    # 3. 判断手机号 是否 重复 mobiles/(?P<mobile>1[3-9]\d{9})/count/
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),

    # 4.登陆页面显示 login/
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # 5.退出登陆
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # 6.用户中心 info/
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),

    # 7.新增邮箱 emails/
    url(r'^emails/$', views.EmailView.as_view(), name='emails'),

    # 8.激活邮箱  emails/verification/
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),

    # 9. 收货地址  address/
    url(r'^address/$', views.AddressView.as_view(), name='address'),

    # 10. 新增 收货地址 addresses/create/
    url(r'^addresses/create/$', views.AddressCreateView.as_view()),

    # 11. 修改密码 password/
    url(r'^password/$', views.ChangePwdView.as_view(), name='password'),

    # 12.保存用户浏览记录 browse_histories/
    url(r'^browse_histories/$', views.UserBrowseHistory.as_view()),

    # 13.忘记密码页面显示 find_password/
    url(r'^find_password/$', views.UserFindPassword.as_view()),

    # 14.验证用户是否存在 accounts/(?P<username>[a-zA-Z0-9_-]{5,20})/sms/token/
    url(r'^accounts/(?P<username>[a-zA-Z0-9_-]{5,20})/sms/token/$', views.UsernameExistView.as_view()),

    # 15.新接口获取短信验证码 find_password_sms_codes/(?P<mobile>1[3-9]\d{9})/
    url(r'^find_password_sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SendSmsView.as_view()),

    # 16.第二个 下一步 提交  accounts/(?P<mobile>[a-zA-Z0-9_-]{5,20})/password/token/
    url(r'^accounts/(?P<mobile>[a-zA-Z0-9_-]{5,20})/password/token/$', views.SendSmsCommiteView.as_view()),

    # 第三步提交 users/(?P<user_id>\d+)/new_password/
    url(r'^users/(?P<user_id>\d+)/new_password/$', views.NewPasswordCommiteView.as_view()),

]
