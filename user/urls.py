from django.urls import path
from .views import registration,update_user_account,UserLoginView,user_logout,activate,pass_change,profile

urlpatterns = [
    path('register/', registration , name = 'register'),
    path('update/<int:user_id>/', update_user_account , name = 'update_account'),
    path('login/', UserLoginView.as_view() , name = 'login'),
    path('logout/', user_logout , name = 'logout'),
    path('profile/', profile , name = 'profile'),
    path('change_password/', pass_change , name = 'password_change'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
]