from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import UserCreateForm as SignUpForm
from .tokens import account_activation_token
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from .forms import MyChangeFormPassword
from .forms import ValidateUsername
from .forms import ChangeForgetPasswordForm

User = get_user_model()


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


def signup(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile", username = request.user.username)
    else:

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.email = user.username
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your Gitlab Account :)'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return redirect('accounts:account_activation_sent')
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})




class AccountActivationSent(TemplateView):
    template_name = 'registration/account_activation_sent.html'




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:activated')
    else:
        return render(request, 'registration/account_activation_invalid.html')



class Activated(TemplateView):
    template_name = 'registration/successful_activation.html'



@login_required
def profile_view(request,username):
    template_name = 'registration/profile.html'
    content = {
    }
    return render(request,template_name,content)



@login_required
def change_password(request, username):
    user = get_object_or_404(User,username=username)
    form = MyChangeFormPassword(user)

    if request.method=="POST":
        form = MyChangeFormPassword(user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile', username = user.username)

    return render(request,'registration/newpassword.html',{'form' : form})


def validate_username(request):
    form = ValidateUsername()

    if request.method == "POST":
        form = ValidateUsername(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username = username)
            current_site = get_current_site(request)
            subject = 'Change Your Gitlab password'
            message = render_to_string('registration/forgot_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('accounts:account_activation_sent')


    return render(request, 'registration/validate_username.html', {'form':form})


def forgot_password(request,uidb64,username,token):
    template = 'registration/newpassword.html'
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {}
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        login(request, user)
        context['validlink'] = True
        form = ChangeForgetPasswordForm(user)

        context['form'] = form
        if request.method == 'POST':
            form = ChangeForgetPasswordForm(user,data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                return redirect('accounts:profile', username=user.username)
            else:
                context['form'] = form

    else:
        context['validlink'] = False


    return render(request,template,context)

