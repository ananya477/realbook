from django.contrib import admin
from .models import Property, Booking, Review, Wishlist

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'property_type', 'status', 'owner', 'created_at')
    list_filter = ('property_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'check_in', 'check_out', 'status', 'booking_date')
    list_filter = ('status', 'booking_date')
    search_fields = ('property__title', 'user__username')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('property__title', 'user__username', 'comment')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'property__title')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)