"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from boards.views import home, board_topic,new_topic,topic_posts,reply_topic,PostUpdateView
from accounts.views import signup
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='', view = home,name='home'),
    path(route='board/<int:pk>', view = board_topic,name='board_topics'),
    path(route='board/<int:pk>/new', view = new_topic,name='new_topic'),
    path(route='board/<int:pk>/topic/<int:topic_pk>', view = topic_posts,name='topic_posts'),
    path(route='board/<int:pk>/topic/<int:topic_pk>/reply/', view = reply_topic,name='reply_topic'),
    path(route='board/<int:pk>/topic/<int:topic_pk>/posts/<int:post_pk>/edit', view = PostUpdateView.as_view(),name='edit_post'),

    # Accounts
    path(route='signup/', view = signup,name='signup'),
    path(route='logout/', view = LogoutView.as_view(),name='logout'),
    path(route='login/', view = LoginView.as_view(template_name='login.html'),name='login'),

    # Reset password
    path(route='reset/',view=PasswordResetView.as_view(template_name='password_reset.html',email_template_name='password_reset_email.html',subject_template_name='password_reset_subject.txt'),name='password_reset'),
    path(route='reset/done/',view=PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path(route='reset/<uidb64>/<token>/',view=PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,60})/$',PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path(route='reset/complete/',view=PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path(route='settings/password/',view=PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
    path(route='settings/password/done/',view=PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
    
]


