from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage

from .models import DB2User
from .tokens import account_activation_token

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import UserLoginForm, UserCreationForm


def login_view(request):
    if not request.user.is_authenticated:
        next_page = request.GET.get('next')
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            if next_page:
                return redirect(next_page)
            return redirect('posts:list_view')
        context = {
            'form': form,
        }
        return render(request, 'db2users/login.html', context)
    else:
        return redirect('posts:list_view')


def signup_view(request):
    if not request.user.is_authenticated:
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.clean_password2()
            user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('db2users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Accout activation.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'db2users/confirm.html')
        else:
            form = UserCreationForm()
        return render(request, 'db2users/signup.html', {'form': form})
    else:
        return redirect('posts:list_view')


def activate(request, uidb64, token):
    if not request.user.is_authenticated:
        next_page = request.GET.get('next')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = DB2User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, DB2User.DoesNotExist):
            user = None
        if user and account_activation_token.check_token(user, token):
            user.activated = True
            user.save()
            if next_page:
                return redirect(next_page)
            else:
                return redirect('account:login')
        else:
            return HttpResponseRedirect('Activation link is invalid!')
    else:
        return redirect('posts:list_view')


def logout_view(request):
    logout(request)
    return redirect('account:login')
