from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, ShippingAddressForm
from .models import Profile, ShippingAddress
from django.shortcuts import get_object_or_404


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'user': request.user,
    }
    return render(request, 'account/profile.html', context)

@login_required
def profile_update_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    shipping_address, created = ShippingAddress.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        address_form = ShippingAddressForm(
            request.POST, 
            instance=request.user.shipping_address
        )
        
        if all([user_form.is_valid(), profile_form.is_valid(), address_form.is_valid()]):
            user_form.save()
            profile_form.save()
            address_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        address_form = ShippingAddressForm(instance=request.user.shipping_address)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
    }
    return render(request, 'account/profile_update.html', context)