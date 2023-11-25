import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.core.paginator import Paginator

from .models import User, Post, Comment


def index(request):
    feed = Post.objects.all().order_by("id").reverse()
    #paginator
    paginator = Paginator(feed, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    if request.user.is_authenticated:
        own_posts   = Post.objects.filter(user=request.user)
        logged_user = request.user
        followers   = logged_user.followers.all()
        following   = logged_user.following.all()

        return render(request, "network/index.html", {
            "feed"      : feed,
            "page_obj"  : page_obj,
            "own_posts" : own_posts,
            "followers" : followers,
            "following" : following,
        })

    else:
        followers = User.objects.all()
        following = User.objects.all()
        feed = Post.objects.all().order_by("id").reverse()

        return render(request, "network/index.html", {
            "feed"      : feed,
            "page_obj"  : page_obj,
            "followers" : followers,
            "following" : following,
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# -------------------------------------------------------- NEW FUNCTIONS -------------------------------------------------------------------
def index_following(request):
    #Base info
    own_posts   = Post.objects.filter(user=request.user)
    logged_user = request.user
    followers   = logged_user.followers.all()
    following   = logged_user.following.all()

    posts_list = []
    #getting all posts in a list
    for user in following:
        for post in Post.objects.filter(user=user):
            posts_list.append(post)

    #getting all ids of the posts in a list
    posts_ids = []
    for post in posts_list:
        posts_ids.append(post.id)

    #passing a list of ids to filter
    feed = Post.objects.filter(pk__in=posts_ids)
    feed.order_by("id").reverse()
    '''
    #feed=Post.objects.none()
    feed=[]
    for i in following:
        group = Post.objects.filter(user=i)
        #feed.union(group)
        feed.append(group)
    '''

    #paginator
    paginator = Paginator(feed, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "feed"      : feed,
        "page_obj"  : page_obj,
        "own_posts" : own_posts,
        "followers" : followers,
        "following" : following,
    })



def search(request):
    if request.method=="POST":
        #getting searched phrase
        searched_phrase=request.POST['q']
        #getting posts only from that user
        searched_users_list = []
        all_users_objects = User.objects.all()
        all_users_names =[]
        #getting all usernames
        for i in all_users_objects:
            all_users_names.append(i.username)
        #comparing the phrase & usernames
        for i in all_users_names:
            if searched_phrase in i:
                searched_users_list.append(i)
        #getting ids from searched usernames
        searched_users_id_list =[]
        for i in searched_users_list:
            id = User.objects.get(username=i)
            searched_users_id_list.append(id)

        #filtering feed
        feed=[]
        for i in searched_users_id_list:
            posts = Post.objects.filter(user=i)
            feed.append(posts)
        #deleting empty
        for i in feed:
            if i == "<QuerySet []>":
                feed.remove(i)

        #some not so nice formatting
        feed2=[]
        for i in feed:
            for j in i:
                feed2.append(j)

        #paginator
        paginator = Paginator(feed2, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        #getting other data
        own_posts = Post.objects.filter(user=request.user)
        logged_user=request.user
        followers=logged_user.followers.all()
        following=logged_user.following.all()
        return render(request, "network/index.html", {
            "feed"      : feed2,
            "page_obj"  : page_obj,
            "own_posts" : own_posts,
            "followers" : followers,
            "following" : following
        })


# --- --- --- FEED --- --- --- #

def get_feed(request, user_id):

    # Show general or particular (given user's) feed
    logged_user=User.objects.get(pk=user_id)
    following=logged_user.following
    if logged_user is not None:
        feed = Post.objects.filter(
            user=user_id)
    elif logged_user is None:
        feed = Post.objects.all()
    else:
        return JsonResponse({"error": "Invalid feed."}, status=400)

    # Return posts in reverse chronologial order
    feed = feed.order_by("-date").all()
    return JsonResponse([post.serialize() for post in feed], safe=False)


# --- --- --- FOLLOWERS/FOLLOWING --- --- --- #

def get_followers_list(request):
    if request.method == "GET":
        # Show all users or only followers
        logged_user=request.user
        if logged_user is not None:
            followers=logged_user.followers.all()
            following=logged_user.following.all()
        elif logged_user is None:
            followers = User.objects.all()
            following = User.objects.all()

        feed = Post.objects.all().order_by("id").reverse()
        user=request.user
        return render(request, "network/index.html", {
                "feed" : feed,
                "user" : user,
                "followers" : followers,
                "following" : following,
                })

def get_following_list(request):
    if request.method == "GET":
        # Show all users or only followers
        logged_user=request.user
        if logged_user is not None:
            following = logged_user.following.all()
            followers = logged_user.followers.all()
        elif logged_user is None:
            following = User.objects.all()
            followers = User.objects.all()

        posts_list = []
        #getting all posts in a list
        for user in following:
            for post in Post.objects.filter(user=user):
                posts_list.append(post)

        #getting all ids of the posts in a list
        posts_ids = []
        for post in posts_list:
            posts_ids.append(post.id)

        #passing a list of ids to filter
        feed = Post.objects.filter(pk__in=posts_ids)
        feed.order_by("id").reverse()

        #paginator
        paginator = Paginator(feed, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        user=request.user
        return render(request, "network/index.html", {
            "feed"      : feed,
            "page_obj"  : page_obj,
            "user"      : user,
            "following" : following,
            "followers" : followers,
            })


@login_required
def follow_user(request, another_user_id, logged_user_id):
    #query for requested profile:
    try:
        logged_user = request.user
    except User.DoesNotExist:
        return JsonResponse({"error": "User profile not found."}, status=404)

    #return user profile contents
    if request.method == "GET":
        return JsonResponse(logged_user.serialize())

    elif request.method == "PUT":
        # Get contents of following another user
        logged_user             = request.user
        data                    = json.loads(request.body)
        logged_user_following   = data.get("following", "")

        # Change users data
        logged_user.following.clear()
        for i in logged_user_following:
            logged_user.following.add(i)
        logged_user.save()

        return JsonResponse({"message": "Follow exchanged successfully."}, status=201)

@login_required
def get_followed(request, another_user_id, logged_user_id):
    #query for requested profile:
    try:
        another_user = User.objects.get(pk=another_user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User profile not found."}, status=404)

    #return user profile contents
    if request.method == "GET":
        return JsonResponse(another_user.serialize())

    elif request.method == "PUT":
        # Get contents of following another user
        another_user            = User.objects.get(pk=another_user_id)
        data                    = json.loads(request.body)
        another_user_followers  = data.get("followers", "")

        # Change users data
        another_user.followers.clear()
        for i in another_user_followers:
            another_user.followers.add(i)
        another_user.save()

        return JsonResponse({"message": "Follow exchanged successfully."}, status=201)

# --- --- --- EDIT PROFILE --- --- --- #

def edit_profile(request, user_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            #return render(request, "network/index.html")
            user=request.user
            feed = Post.objects.all().order_by("id").reverse()
            if request.user.is_authenticated:
                return render(request, "network/index.html", {
                    "feed": feed,
                    "user" : user,
                    })
            else:
                return render(request, "network/login.html")

        # Composing a new post must be via POST
        elif request.method == "POST":
            user            = request.user
            new_first_name      = request.POST['first_name']
            new_last_name       = request.POST['last_name']
            new_email           = request.POST['email']
            new_bio             = request.POST['bio']

            #alter user
            user.first_name         = new_first_name
            user.last_name          = new_last_name
            user.email              = new_email
            user.bio                = new_bio

            #checking photo
            new_profile_photo   = request.FILES.get('profile_photo')
            if new_profile_photo == None:
                pass
            else:
                user.profile_photo      = new_profile_photo

            #save?
            user.save()

            #redirect back
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html")


def view_profile(request, user_id):
    #query for requested profile:
    try:
        other_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User profile not found."}, status=404)

    #return user profile contents
    if request.method == "GET":
        return JsonResponse(other_user.serialize())


# --- --- --- NEW POST --- --- --- #

def new_post(request):
    if request.method == "GET":
        return render(request, "network/index.html")

    # Composing a new post must be via POST
    elif request.method == "POST":
        # Get contents of post
        user            = request.user
        description     = request.POST['post_description']
        date            = datetime.datetime.now()
        photo           = request.FILES.get('post_photo')

        #checking if there are both photo & text:
        if photo == None or description == None:
            return JsonResponse({"error": "New post must include both photo and text."}, status=404)

        # Create post
        post = Post(
            user=user,
            description=description,
            date=date,
            photo=photo,
        )
        post.save()

        #add post id to user post field
        user.posts.add(post)

        return HttpResponseRedirect(reverse("index"))

# --- --- --- EDIT OWN POST --- --- --- #
@csrf_exempt
def edit_post(request, post_id):
    if request.method == "GET":
        #try to get the post
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        #check if the logged user is accessing their own post
        logged_user = request.user
        if logged_user.id != post.user.id:
            return JsonResponse({"error": "Cannot edit another person's post"}, status=404)

        #rendering basic pages
        feed        = Post.objects.all().order_by("id").reverse()
        #paginator
        paginator = Paginator(feed, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        followers   = logged_user.followers.all()
        following   = logged_user.following.all()

        return JsonResponse(post.serialize())

    elif request.method == "POST":
        #try to get the post
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        # Get contents of post
        new_description = request.POST["new_post_description_textarea"]
        new_photo = request.FILES.get("new_post_photo")
        '''
        data        = json.loads(request.body)
        new_description = data.get("description", "")
        new_photo       = data.get("photo", "")
        '''
        # alter post
        post.description = new_description
        if new_photo == None:
            pass
        else:
            post.photo = new_photo

            #post.photo.url = new_photo
        #save
        post.save()
        return HttpResponseRedirect(reverse("index"))

def edit_postP(request, post_id):
    if request.method == "POST":
        #try to get the post
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        # Get contents of post
        #new_description = request.POST["new_post_description"]
        new_description = request.Get.get("new_post_description")
        new_photo = request.FILES.get("new_post_photo")
        '''
        data        = json.loads(request.body)
        new_description = data.get("description", "")
        new_photo       = data.get("photo", "")
        '''
        # alter post
        post.description = new_description
        if new_photo == None:
            pass
        else:
            post.photo = new_photo

            #post.photo.url = new_photo
        #save
        post.save()
        return JsonResponse({"message": "Post saved successfully."}, status=201)


# --- --- --- COMMENT --- --- --- #

def view_post(request, post_id):
    #query for requested post:
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    #return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

def commentP(request):
    # Composing a new comment must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of comment
    data            = json.loads(request.body)
    comment_text    = data.get("text", "")
    post_id         = data.get("post_id","")
    post            = Post.objects.get(pk=post_id)
    logged_user     = request.user
    user_photo      = logged_user.profile_photo.url

    # Create comment
    comment = Comment(
        user        = logged_user,
        user_photo  = user_photo,
        text        = comment_text
        )
    comment.save()
    #add comment id to post  comments field
    post.comments.add(comment)

    return JsonResponse({"message": "Post saved successfully."}, status=201)


def comment_list(request, comment_id):
    #query for requested comment:
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found."}, status=404)
    #return comment contents
    if request.method == "GET":
        return JsonResponse(comment.serialize())


def like_unlike(request, post_id, logged_user_id):
    #query for requested post:
    try:
        user = User.objects.get(pk=logged_user_id)
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    #return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        liked_by_list = data.get("liked_by", "")

         # Change post data
        post.liked_by.clear()
        for i in liked_by_list:
            post.liked_by.add(i)
        post.save()

        return JsonResponse({"message": "Post liked/unliked successfully."}, status=201)








