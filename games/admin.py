from django.contrib import admin

from games.models import Category, Game, GameImage


class GameImageInline(admin.TabularInline):
    model = GameImage


class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['id', 'name']
    list_filter = ['category']
    search_fields = ['name', 'description']
    inlines = [GameImageInline]


admin.site.register(Category)
admin.site.register(Game)
admin.site.register(GameImage)
