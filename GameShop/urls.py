from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from games.views import MainPageView
from order.views import ActivateOrderView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='home'),
    path('games/', include('games.urls')),
    path('user/', include('user.urls')),
    path('cart/', include('order.urls')),
    path('order/activate/<str:activation_code>/', ActivateOrderView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
