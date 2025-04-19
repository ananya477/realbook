from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from . import views  # Add this import

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile'),
    
    # Property URLs
    path('property/new/', views.property_create, name='property-create'),
    path('property/<int:pk>/', views.property_detail, name='property-detail'),
    path('property/<int:pk>/update/', views.property_update, name='property-update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property-delete'),
    
    # Wishlist URLs
    path('property/<int:pk>/wishlist/add/', views.add_to_wishlist, name='add-to-wishlist'),
    path('property/<int:pk>/wishlist/remove/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('property/<int:pk>/wishlist/add/', views.add_to_wishlist, name='add-to-wishlist'),
    path('property/<int:pk>/wishlist/remove/', views.remove_from_wishlist, name='remove-from-wishlist'),
    
    # Booking URLs
    path('property/<int:pk>/book/', views.create_booking, name='create-booking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)