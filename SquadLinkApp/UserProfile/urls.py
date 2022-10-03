from django.urls import path
from .views import SquadLinkUserLogInView, SquadLinkUserCreationView, SquadLinkUserView

app_name = 'UserProfile'

urlpatterns = [
    path('create/', SquadLinkUserCreationView.as_view(), name='add-profile'),
    path('log-in/', SquadLinkUserLogInView.as_view(), name='log-in'),
    path('view', SquadLinkUserView.as_view(), name='view-profile')
]
