from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.crypto import get_random_string

from games.models import Game

User = get_user_model()


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, game_id, quantity, price):
        product_id = str(game_id)
        if game_id not in self.cart:
            self.cart[game_id] = {
                'quantity': quantity,
                'price': price
            }
        self.save()

    def remove(self, game_id):
        game_id = str(game_id)
        if game_id in self.cart:
            del self.cart[game_id]
            self.save()

    def clean(self):
        for game_id in self.cart:
            self.remove(game_id)

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        game_ids = self.cart.keys()
        games = Game.objects.filter(id__in=game_ids)
        for game in games:
            self.cart[str(game.id)]['game'] = game

        for item in self.cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price'] * item['quantity'])
                   for item in self.cart.values())



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True, null=True)

    def create_activation_code(self):
        code = get_random_string(8)
        self.activation_code = code
        self.save()

    def send_activation_mail(self):
        message = f'http:/localhost:8000/order/activate/{self.activation_code}/'
        send_mail(
            'Подтверждение заказа',
            message,
            'test@gmail.com',
            [self.user.email]
        )

    def send_mail(self):
        if self.is_active:
            message = 'Ваш заказ принят!'
            send_mail(
                'Заказ',
                message,
                'test@gmail.com',
                [self.user.email]
            )
        else:
            message = 'Ваш заказ не подтвержден. Пожалуйста, подтвердите заказ.'
            send_mail(
                'Заказ',
                message,
                'test@gmail.com',
                [self.user.email]
            )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(validators=[MaxValueValidator(20)])


