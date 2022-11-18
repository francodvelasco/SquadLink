from django.urls import path
from .views import SquadLinkAddFriendsHandler, SquadLinkConfirmFriendsHandler, SquadLinkUserLogInView, SquadLinkUserCreationView, SquadLinkUserSquadsView, SquadLinkUserView, SquadLinkUserEditView

app_name = 'UserProfile'

urlpatterns = [
    path('register/', SquadLinkUserCreationView.as_view(), name='register'),
    path('sign-in/', SquadLinkUserLogInView.as_view(), name='sign-in'),
    path('view', SquadLinkUserView.as_view(), name='view-profile'),
    path('edit', SquadLinkUserEditView.as_view(), name='edit-profile'),
    path('my-squads', SquadLinkUserSquadsView.as_view(), name='view-squads'),
    path('add-friend/<int:sender>/<int:receiver>', SquadLinkAddFriendsHandler.as_view(), name='add-friend'),
    path('confirm-friend/<int:sender>/<int:receiver>', SquadLinkConfirmFriendsHandler.as_view(), name='confirm-friend')
]
