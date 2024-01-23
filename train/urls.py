from django.urls import path
from .views import TrainDisplay,details,user_comment,search

urlpatterns = [
    path('', TrainDisplay.as_view(), name='train_list'),
    path('category/<slug:station_slug>/', TrainDisplay.as_view(), name='train_list_by_category'),
    path('details/<int:id>/', details, name='train_details'),
    path('comment/<int:id>/', user_comment, name='comment'),
    path('search/', search , name='search'),
]