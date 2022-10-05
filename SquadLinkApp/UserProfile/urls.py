from django.urls import path
from .views import SquadLinkUserLogInView, SquadLinkUserCreationView, SquadLinkUserView

app_name = 'UserProfile'

urlpatterns = [
    path('register/', SquadLinkUserCreationView.as_view(), name='register'),
    path('sign-in/', SquadLinkUserLogInView.as_view(), name='sign-in'),
    path('view', SquadLinkUserView.as_view(), name='view-profile')
]
