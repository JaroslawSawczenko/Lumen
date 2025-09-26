from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile' : profile,
    }
    return render(request, 'users/profile.html', context)






