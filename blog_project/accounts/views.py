from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from accounts.forms import RegistrationForm
from accounts.tokens import account_activation_token
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from blog.views import post_list_view
from django.contrib.auth.decorators import login_required


def activation_sent_view(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/activation_sent.html')
    else:
        messages.warning(request, "This is wrong path")
        return render(request,"accounts/login.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        user.save()
        login(request, user)
        #messages.success(request, f"New account created: {username}")
    else:
        messages.error(request, f"link is deactived")
    return render(request,"accounts/login.html")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('post_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request,'accounts/login.html')

def ragister_view(request):
    form=RegistrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if email and User.objects.filter(email=email):
                     messages.error(request, "Email addresses must be unique.")
                     return render(request,'accounts/login.html')
            user = form.save()
            username = form.cleaned_data.get('username')
            print(username)
            #login(request, user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('accounts/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(subject, message,'1857harshitgupta@gmail.com',[to_email])
            return redirect('activation_sent')
        else:
            messages.error(request, "username must be unique.")
    return render(request,"accounts/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request,"accounts/login.html")

