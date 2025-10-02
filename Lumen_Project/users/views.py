from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, SignUpForm
from django.contrib import messages
from .models import UserProfile
from Lumen.models import QuizResult
from django.http import HttpRequest, HttpResponse

def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto dla {username} zostało pomyślnie utworzone! Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Twój profil został zaktualizowany!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    quiz_results = QuizResult.objects.filter(user=request.user).order_by('-completed_at')

    context = {
        'profile': profile,
        'form': form,
        'quiz_results': quiz_results,
    }
    return render(request, 'users/profile.html', context)