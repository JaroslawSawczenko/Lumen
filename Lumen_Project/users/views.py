from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from Lumen.models import QuizResult


@login_required
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    quiz_results = QuizResult.objects.filter(user=request.user).order_by('-completed_at')

    context = {
        'profile' : profile,
        'form': form,
        'quiz_results' :quiz_results,
    }
    return render(request, 'users/profile.html', context)






