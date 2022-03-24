from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('item/<str:pk>', views.item, name="item"),
    path('', views.home, name="home"),
    path('create-item/', views.createItem, name="createItem"),
    path('update-item/<str:pk>/', views.updateItem, name="updateItem"),
    path('delete-item/<str:pk>/', views.deleteItem, name="deleteItem"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('add-item/', views.addItem, name="addItem"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)