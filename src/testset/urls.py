from django.urls import path

from . import views

app_name = 'testset'

urlpatterns = [
    path('list', views.TestListView.as_view(), name='list'),
    path('leader', views.UserLeaderBoardListView.as_view(), name='leader_bord'),
]