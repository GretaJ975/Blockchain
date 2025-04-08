from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import  block_detail, about, index, view_chain, order_list, mine, RegisterView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('', index, name='index'),
    path('create/', views.create_blockchain_entry, name='create'),
    path('block/<int:block_id>/', block_detail, name='block_detail'),
    path('create_block/', views.create_block, name='create_block'),
    path('create_mine/', views.create_mine, name='create_mine'),
    path('mine/', mine, name='mine'),
    path('about/', about, name='about'),
    path('chain/', view_chain, name='view_chain'),
    path('orders/', order_list, name='orders'),
    path('order/<int:pk>/', views.OrderDetailView, name='order_detail'),
    path('create-order/', views.create_order, name='create_order'),
    path('block/', views.block, name='block'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', RegisterView.as_view(), name='register'),
    path("profile/", views.show_profile, name="profile"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)