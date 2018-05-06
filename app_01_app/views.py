from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from app_01_app.forms import AuthenticateForm, UserCreateForm, app_01Form
from app_01_app.models import app_01


def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated:
        app_01_form = app_01Form()
        user = request.user
        app_01s_self = app_01.objects.filter(user=user.id)
        app_01s_buddies = app_01.objects.filter(user__userprofile__in=user.profile.follows.all())
        app_01s = app_01s_self | app_01s_buddies

        return render(request,
                      'buddies.html',
                      {'app_01_form': app_01_form, 'user': user,
                       'app_01s': app_01s,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')


@login_required
def public(request, app_01_form=None):
    app_01_form = app_01_form or app_01Form()
    app_01s = app_01.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'app_01_form': app_01_form, 'next_url': '/app_01s',
                   'app_01s': app_01s, 'username': request.user.username})


@login_required
def submit(request):
    if request.method == "POST":
        app_01_form = app_01Form(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if app_01_form.is_valid():
            app_01 = app_01_form.save(commit=False)
            app_01.user = request.user
            app_01.save()
            return redirect(next_url)
        else:
            return public(request, app_01_form)
    return redirect('/')


def get_latest(user):
    try:
        return user.app_01_set.order_by('id').reverse()[0]
    except IndexError:
        return ""


@login_required
def users(request, username="", app_01_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        app_01s = app_01.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile
            return render(request, 'user.html', {'user': user, 'app_01s': app_01s, })
        return render(request, 'user.html', {'user': user, 'app_01s': app_01s, 'follow': True, })
    users = User.objects.all().annotate(app_01_count=Count('app_01'))
    app_01s = map(get_latest, users)
    obj = zip(users, app_01s)
    app_01_form = app_01_form or app_01Form()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'app_01_form': app_01_form,
                   'username': request.user.username, })


@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')
