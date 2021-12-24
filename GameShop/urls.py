
from django.contrib import admin
from django.urls import path

from games.views import GameListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('games/', GameListView.as_view(), name='games-list'),
]
