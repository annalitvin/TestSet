from django.urls import path

from . import views

app_name = 'testset'

urlpatterns = [
    path('list', views.TestListView.as_view(), name='list'),
    path('<int:pk>/next', views.TestRunView.as_view(), name='next'),
    path('start/<int:test_pk>', views.TestStartView.as_view(), name='start'),
    path('leader', views.UserLeaderBoardListView.as_view(), name='leader_bord'),
]
