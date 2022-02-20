from django.http import HttpResponse, Http404
from multiprocessing import context
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from socialnetwork.forms import LoginForm, ProfileForm, RegisterForm
from socialnetwork.models import Post, Profile


# Create your views here.


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_profile = Profile()
    new_profile.user = new_user
    new_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

@login_required
def global_action(request):
    if request.method == "GET":
        return render(request, 'socialnetwork/globalStream.html', {'posts': Post.objects.all()})
    
    if 'text' not in request.POST or not request.POST['text']:
        return render(request, 'socialnetwork/globalStream.html', {'posts': Post.objects.all(), 'error': "Post cannot be blank"})

    new_post = Post(text = request.POST['text'], user = request.user, creation_time = timezone.now())
    new_post.save()
    return render(request, 'socialnetwork/globalStream.html', {'posts': Post.objects.all()})

@login_required
def follower_action(request):
    return render(request, 'socialnetwork/followerStream.html', {'posts': Post.objects.all()})

@login_required
def myProfile_action(request):
    if request.method == 'GET':
        context = {'profile': request.user.profile,
                    'form': ProfileForm(initial={'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/myProfile.html', context)
    
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'socialnetwork/myProfile.html', context)
    
    profile = get_object_or_404(Profile, user=request.user)

    profile.bio = form.cleaned_data['bio']
    profile.user = request.user
    profile.picture = form.cleaned_data['picture']
    profile.content_type = form.cleaned_data['picture'].content_type
    profile.save()

    context = {
        'profiles': Profile.objects.all(),
        'form': form,
        'message': 'Profile #{} updated.'.format(profile.id),
    }
    return render(request, 'socialnetwork/myProfile.html', context)

@login_required
def otherProfile_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'socialnetwork/otherProfile.html', {'profile': user.profile})

@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    return render(request, 'socialnetwork/otherProfile.html', {'profile': user_to_unfollow.profile})

@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return render(request, 'socialnetwork/otherProfile.html', {'profile': user_to_follow.profile})

@login_required
def get_photo(request, user_id):
    profile = get_object_or_404(Profile, user=user_id)

    if not profile.picture:
        raise Http404
    return HttpResponse(profile.picture, content_type=profile.content_type)