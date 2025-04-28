# from django.contrib import admin
from django.conf import settings
from django.urls import path
from iceapp import views
from django.conf.urls.static import static



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('index', views.index),
    path('ourstory', views.ourstory),
    path('locations', views.locations),
    path('franchisequeries', views.franchisequeries),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('signup', views.signup),
    path('cart', views.cart),
    path('fruitnnut', views.fruitnnut),
    path('internationalpremium', views.internationalpremium),
    path('internationalclassic', views.internationalclassic),
    path('indianinspiration', views.indianinspiration),
    path('superpremium', views.superpremium),
    path('ordernow/<iid>',views.ordernow),
    path('icecreamdetails/<iid>',views.icecreamdetails),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('remove/<cid>',views.remove),
    path('checkout',views.checkout),
    path('fetchorder',views.fetchorder),
    path('makepayments',views.makepayments),
    path('payment_success',views.payment_success),
    path('user_profile',views.user_profile),
    path('edit_user_profile',views.edit_user_profile),
    path('orderhistory',views.orderhistory),
    path('icecreamdetails2',views.icecreamdetails2),
    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)