from django.urls import path
from .views import GameListCreateAPIView, PlayerListCreateAPIView, GameDetailAPIView

urlpatterns = [
    path('game/', GameListCreateAPIView.as_view(), name='game-list-create'),
    path('game/<int:pk>', GameDetailAPIView.as_view(), name='game-list-create'),
    path('player/<int:game_pk>', PlayerListCreateAPIView.as_view(), name='player-list-create')
]