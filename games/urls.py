from django.contrib import admin
from django.urls import path

from games.views import GameListView, GameDetailsView, CreateGameView, UpdateGameView, DeleteGameView, SearchResultsView

urlpatterns = [
    path('', GameListView.as_view(), name='games-list'),
    path('<int:pk>/', GameDetailsView.as_view(), name='game-details'),
    path('create/', CreateGameView.as_view(), name='create-game'),
    path('update/<int:pk>/', UpdateGameView.as_view(), name='update-game'),
    path('delete/<int:pk>/', DeleteGameView.as_view(), name='delete-game'),
    path('search/', SearchResultsView.as_view(), name='search')
]

