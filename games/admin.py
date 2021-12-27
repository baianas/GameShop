from django.contrib import admin

from games.models import Category, Game, GameImage

admin.site.register(Category)
admin.site.register(Game)
admin.site.register(GameImage)
