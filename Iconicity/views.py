from django.shortcuts import render, resolve_url, reverse
from django.http import HttpResponse
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from .forms import PostsCreateForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import logout
from django.http.request import HttpRequest
from django.views.generic import CreateView
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

#https://thecodinginterface.com/blog/django-auth-part1/

def getAuthor(id):
    author_profile = serializers.serialize("json", UserProfile.objects.filter(uid=id))
    jsonload = json.loads(author_profile)[0]
    raw_id = jsonload['pk']
    jsonload = jsonload['fields']
    temp = str(jsonload['host']) + '/author/' + str(raw_id)
    jsonload['user_id'] = str(jsonload['host']) + '/author/' + str(raw_id)
    jsonload['url'] = jsonload['user_id']
    return Response(jsonload)

def postAuthor(id):
    # update author profile
    pass

# not in use at this moment
class AuthorProfile(APIView):
    # get a author's profile by its id
    def get(self, request, id):
        author_profile = serializers.serialize("json", UserProfile.objects.filter(uid=id))
        jsonload = json.loads(author_profile)[0]
        raw_id = jsonload['pk']
        jsonload = jsonload['fields']
        temp = str(jsonload['host']) + '/author/' + str(raw_id)
        jsonload['user_id'] = str(jsonload['host']) + '/author/' + str(raw_id)
        jsonload['url'] = jsonload['user_id']
        return Response(jsonload)

# get all followers this author has
# id is the author's id
def getFollowers(id):
    authorfollow = getAuthor(id).data['follow'] # return followe list of this author
    # now it should be a list of urls.


    print(type(authorfollow))
    print(authorfollow)
    #print(json.loads(authorfollow))

def logout_view(request):
    # in use, support log out
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-logout-button-in-Django.php
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('login'))


class LoginView(View):
    def get(self, request):
        return render(request, 'Iconicity/login.html', { 'form':  AuthenticationForm })

    def post(self,request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(
                    request,
                    'Iconicity/login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            login(request, form.get_user())

            return redirect(reverse('main_page'))

        return render(request, 'Iconicity/login.html', { 'form': form })

# citation:https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-profile-model


"""TODO:
Question asked by Qianxi:
for the following two lines:

user = authenticate(username=username, password=raw_password)
login(request, user)

we need exception handling.

Finish it and delete this comment block
"""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            User = authenticate(username=username, password=raw_password)
            Github = form.cleaned_data.get('github')
            host = request.get_host()
            createUserProfile(username, User, Github, host)

            login(request, User)
            return redirect('main_page')

    else:
        form = SignUpForm()
    return render(request, 'Iconicity/signup.html', {'form': form})

@login_required
def main_page(request):
    userProfile = getUserProfile(request.user)
    # get all the posts posted by the current user
    obj = getPosts(request.user)
    post_json = json.loads(obj)
    new_list = [i['fields'] for i in post_json]
    context = {
        'posts': new_list,
        'UserProfile': userProfile
    }
    """Note:
    Consider that there are case when there's no posts of this author
    change main_page.html so that it looks better when there's no post for
    from author.

    finish this and delete this comment block.
    """
    return render(request, 'Iconicity/main_page.html', context)


def createUserProfile(Display_name, User, Github, host):
    profile = UserProfile(user=User,
                          display_name=Display_name,
                          github=Github,
                          host=host)
    profile.url = str(host) + '/author/' + str(profile.uid)
    profile.save()

def getUserProfile(currentUser):
    # return a UserProfile object for the current login user
    return UserProfile.objects.filter(user=currentUser).first()

def getPosts(user):
    return serializers.serialize("json", list(Post.objects.filter(author=user.id)))

# @login_required
# def new_post(request):
#     if request.method == "GET":
#         template = "Iconicity/new_post.html"
#         form = PostsCreateForm(request.POST)

#         if form.is_valid():
#             print("True")
#             form.save()

#         else:
#             print(form.errors)
#             form = PostsCreateForm()

#         context = {
#             'form': form,
#         }
#         return render(request, template, context)


class AddPostView(CreateView):
    model = Post
    template= "/Iconicity/post_form.html"
    # fields = "__all__"
    # Post.author = UserProfile.objects.values()['uid']
    def post(self, request):
        print("posting")
        template = "Iconicity/post_form.html"
        form = PostsCreateForm(request.POST, request.FILES,)
        print(request.FILES)
        
        if form.is_valid():
            print("posting...")
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('main_page')

        else:
            print(form.errors)
            form = PostsCreateForm(request.POST)

        context = {
            'form': form,
        }
        return render(request, template, context)

    def get(self, request):
        print("getting")
        return render(request, 'Iconicity/post_form.html', { 'form':  PostsCreateForm })

# By Shway, the friend requests stuff:
def friendRequests_received_view(request):
    profile = getUserProfile(request.user)
    requests = FriendRequest.objects.friendRequests_received(profile)

    context = {'requests': requests}

    return render(request, 'Iconicity/frdRequests.html', context)

def userProfile_list_view(request):
    user = request.user
    profiles = UserProfile.objects.get_all_available_profiles(user)

    context = {'profiles': profiles}

    return render(request, 'Iconicity/profile_list.html', context)