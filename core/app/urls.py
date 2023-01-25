from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Login, Signup,Home,Cart,Checkout

urlpatterns = [
   path('', Home.as_view() , name ='home'), 
   path('signup', Signup.as_view() , name ='signup'),
   path('login/', Login.as_view() , name ='login'),
   path('logout', views.logout, name='logout'),
   path('cart', Cart.as_view(), name='cart'),
   path('checkout', Checkout.as_view(), name='checkout'),   
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
