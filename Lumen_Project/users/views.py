from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponse

from .forms import UserProfileForm, SignUpForm
from .models import UserProfile
from Lumen.models import QuizResult

def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Konto nieaktywne do czasu aktywacji
            user.save()

            # Generowanie linku aktywacyjnego
            current_site = get_current_site(request)
            mail_subject = 'Aktywuj swoje konto w Lumen'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])

            try:
                email.send()
                return render(request, 'registration/registration_pending.html')
            except Exception as e:
                user.delete()
                messages.error(request, f'Błąd wysyłki: {e}. Sprawdź konfigurację SMTP.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Konto aktywne! Możesz się zalogować.')
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')

@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil zaktualizowany!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    quiz_results = QuizResult.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'users/profile.html', {
        'profile': profile,
        'form': form,
        'quiz_results': quiz_results,
    })