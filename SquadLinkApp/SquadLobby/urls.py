from django.urls import path
from .views import *

app_name = 'SquadLobby'

urlpatterns = [
    path('create/', LobbyCreateView.as_view(), name='lobby-create'),
    path('details/<int:pk>', LobbyDetailsView.as_view(), name='lobby-details'),
    path('list/', LobbyListView.as_view(), name='lobby-list'),
    path('search/', LobbySearchView.as_view(), name='lobby-search'),
    path('edit/<int:pk>', LobbyEditView.as_view(), name='lobby-edit')
]