from django.urls import path
from .views import StartChatView, OnlineUsersView

urlpatterns = [
    path("api/chat/start/<int:pk>/", StartChatView.as_view()),
    path('api/online-users', OnlineUsersView.as_view())
]