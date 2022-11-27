from django.urls import path
from .views import *

app_name = 'SquadLobby'

urlpatterns = [
    path('create/', LobbyCreateView.as_view(), name='lobby-create'),
    path('details/<int:pk>', LobbyDetailsView.as_view(), name='lobby-details'),
    path('list/', LobbyListView.as_view(), name='lobby-list'),
    path('list/mysquads', MyLobbyListView.as_view(), name='my-lobby-list'),
    path('search/', LobbySearchView.as_view(), name='lobby-search'),
    path('edit/<int:pk>', LobbyEditView.as_view(), name='lobby-edit'),
    path('kick-user/<int:lobby>/<int:to_kick>', LobbyKickUserHandler.as_view(), name='kick-user'),
    path('transfer-owner/<int:lobby>/<int:transfer_to>', LobbyTransferOwnerHandler.as_view(), name='transfer-owner')
]