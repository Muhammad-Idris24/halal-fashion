from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    # You'll implement proper order logic later
    return render(request, 'orders/history.html', {})