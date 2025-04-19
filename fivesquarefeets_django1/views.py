from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Wishlist, Booking, Review
from .forms import PropertyForm, ReviewForm
from django.utils import timezone  # Add this import

def home(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'fivesquarefeets_django1/home.html', {
        'properties': properties,
        'title': 'Home'
    })

def about(request):
    return render(request, 'fivesquarefeets_django1/about.html', {'title': 'About'})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            messages.success(request, 'Your property has been listed!')
            return redirect('property-detail', pk=property.pk)
    else:
        form = PropertyForm()
    return render(request, 'fivesquarefeets_django1/property_form.html', {'form': form, 'title': 'List Property'})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    reviews = Review.objects.filter(property=property).order_by('-review_date')
    bookings = Booking.objects.filter(property=property, status='confirmed').order_by('check_in')
    is_wishlisted = False
    review_form = ReviewForm()  # Initialize the review form
    
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, property=property).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.property = property
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('property-detail', pk=pk)
    
    context = {
        'property': property,
        'title': property.title,
        'is_wishlisted': is_wishlisted,
        'reviews': reviews,
        'review_form': review_form,
        'bookings': bookings
    }
    return render(request, 'fivesquarefeets_django1/property_detail.html', context)

@login_required
def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.owner != request.user:
        messages.error(request, 'You are not authorized to update this property.')
        return redirect('property-detail', pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your property has been updated!')
            return redirect('property-detail', pk=pk)
    else:
        form = PropertyForm(instance=property)
    return render(request, 'fivesquarefeets_django1/property_form.html', {
        'form': form,
        'title': 'Update Property'
    })

@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.owner != request.user:
        messages.error(request, 'You are not authorized to delete this property.')
        return redirect('property-detail', pk=pk)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Your property has been deleted!')
        return redirect('home')
    return render(request, 'fivesquarefeets_django1/property_confirm_delete.html', {
        'property': property,
        'title': 'Delete Property'
    })


@login_required
def add_to_wishlist(request, pk):
    property = get_object_or_404(Property, pk=pk)
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        property=property
    )
    if created:
        messages.success(request, 'Property added to your wishlist!')
    else:
        messages.info(request, 'Property is already in your wishlist!')
    return redirect('property-detail', pk=pk)

@login_required
def remove_from_wishlist(request, pk):
    property = get_object_or_404(Property, pk=pk)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, property=property)
    wishlist_item.delete()
    messages.success(request, 'Property removed from your wishlist!')
    return redirect('property-detail', pk=pk)

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'fivesquarefeets_django1/wishlist.html', {
        'wishlist_items': wishlist_items,
        'title': 'My Wishlist'
    })


@login_required
def create_booking(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        # Check if dates are valid
        if check_in and check_out:
            check_in_date = timezone.datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = timezone.datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Check if the dates are not in the past
            if check_in_date < timezone.now().date():
                messages.error(request, 'Check-in date cannot be in the past.')
                return redirect('property-detail', pk=pk)
            
            # Check if check-out is after check-in
            if check_out_date <= check_in_date:
                messages.error(request, 'Check-out date must be after check-in date.')
                return redirect('property-detail', pk=pk)
            
            # Check if property is available for these dates
            existing_bookings = Booking.objects.filter(
                property=property,
                check_in__lte=check_out_date,
                check_out__gte=check_in_date
            )
            
            if existing_bookings.exists():
                messages.error(request, 'Property is not available for these dates.')
                return redirect('property-detail', pk=pk)
            
            # Create the booking
            booking = Booking.objects.create(
                property=property,
                user=request.user,
                check_in=check_in_date,
                check_out=check_out_date,
                status='pending'
            )
            
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('property-detail', pk=pk)
        else:
            messages.error(request, 'Please select both check-in and check-out dates.')
            
    return render(request, 'fivesquarefeets_django1/booking_form.html', {
        'property': property,
        'title': f'Book {property.title}'
    })