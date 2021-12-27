from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from order.forms import AddToCartForm

from games.models import Game
from order.models import Cart, Order, OrderItem



class AddToCartView(View):
    def post(self, request, game_id):
        cart = Cart(request)
        game = get_object_or_404(Game, id=game_id)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quantity = data.get('quantity')
            cart.add(game.id, quantity, str(game.price))
        return redirect(reverse_lazy('cart-details'))


class RemoveFromCartView(View):
    def get(self, request, game_id):
        cart = Cart(request)
        game = get_object_or_404(Game, id=game_id)
        cart.remove(game.id)
        return redirect(reverse_lazy('cart-details'))


class CartDetailsView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'order/cart_details.html', {'cart': cart})


class IncrementQuantityView(View):
    def get(self, request, game_id):
        cart = Cart(request)
        game = get_object_or_404(Game, id=game_id)
        cart.increment_quantity(game.id)
        return redirect(reverse_lazy('cart-details'))


class CreateOrderView(View):
    def get(self, request):
        session_cart = Cart(request)
        if not session_cart.cart:
            return redirect(reverse_lazy('index'))
        order = Order(user=request.user, total_price=session_cart.get_total_price())
        for id, values in session_cart.cart.items():
            game = Game.objects.get(id=id)
            OrderItem(order=order, game=game, quantity=values.get("quantity"))
        session_cart.clean()
        order.send_activation_mail()


class ActivateOrderView(View):
    def get(self, request, activation_code):
        order = Order.objects.get(user=request.user, activation_code=activation_code)
        order.is_active = True
        order.save()
        order.send_mail()

