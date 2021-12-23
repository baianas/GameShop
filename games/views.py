from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from games.forms import GameForm
from games.models import Game


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff


class CreateGameView(CreateView):
    queryset = Game.objects.all()
    template_name = 'games/create_game.html'
    form_class = GameForm
    success_url = reverse_lazy('games-list')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save()
            for image in request.FILES.getlist('game_image'):
                GameImage.objects.create(game=game, image=image)
            return redirect(game.get_absolute_url())
        return self.form_invalid(form)