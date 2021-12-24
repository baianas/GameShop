from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from games.forms import GameForm, GameImageForm
from games.models import Game, GameImage


class GameListView(ListView):
    queryset = Game.objects.all()
    template_name = 'game/games_list.html'
    context_object_name = 'games'
    paginate_by = 8

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['cart_form']


class GameDetailsView(DetailView):
    queryset = Game.objects.all()
    template_name = 'game/game_details.html'
    context_object_name = 'game'


ImageFormSet = modelformset_factory(GameImage,
                                    form=GameImageForm,
                                    extra=3,
                                    max_num=5,
                                    can_delete=True)


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


class UpdateGameView(IsAdminMixin, UpdateView):
    queryset = Game.objects.all()
    form_class = GameForm
    template_name = 'game/update_game.html'
    context_object_name = 'game'


class DeleteGameView(IsAdminMixin, DeleteView):
    queryset = Game.objects.all()
    form_class = GameForm
    template_name = 'game/delete_game.html'
    context_object_name = 'games-list'


class IndexPageView(TemplateView):
    template_name = 'game/index.html'
