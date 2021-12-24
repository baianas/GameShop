from django import forms

from games.models import Game, GameImage


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'price', 'category']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Цена должна быть положительной')
        return price


class GameImageForm(forms.ModelForm):
    class Meta:
        model = GameImage
        fields = ['image']
