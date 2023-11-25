from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    id              = models.AutoField(primary_key=True)
    profile_photo   = models.ImageField(
        upload_to='user_profiles',
        height_field=None,
        width_field=None,
        default='network/static/User01.png'
        )
    bio             = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    followers       = models.ManyToManyField('network.User', related_name='user_followers', blank=True)
    following       = models.ManyToManyField('network.User', related_name='user_following', blank=True)
    posts           = models.ManyToManyField('network.Post', related_name='users_posts', blank=True)

    def get_number_followers(self):
        list_followers=[]
        for i in self.followers.all():
            list_followers.append(i.username)
        return int(len(list_followers))

    def get_number_following(self):
        list_following=[]
        for i in self.following.all():
            list_following.append(i.username)
        return int(len(list_following))

    def get_number_posts(self):
        list_posts=[]
        for i in self.posts.all():
            list_posts.append(i.id)
        return int(len(list_posts))

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "profile_photo": self.profile_photo.url,
            "bio": self.bio,
            "followers": [user.id for user in self.followers.all()],
            "following": [user.id for user in self.following.all()],
            "posts": [post.id for post in self.posts.all()]
        }


class Post(models.Model):
    id          = models.AutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True)
    description = models.CharField(max_length=280)
    date        = models.DateField(auto_now_add=True)
    photo       = models.ImageField(
        upload_to='images_uploaded',
        height_field=None,
        width_field=None,
        default='network/static/post_01.jpg'
        )
    liked_by    = models.ManyToManyField(User, related_name='upvoter', blank=True)
    comments    = models.ManyToManyField('network.Comment', related_name='post_comment', blank=True)

    def __str__(self):
        return f"{self.user}'s post of id: {self.id}"

    def get_number_likes (self):
        list_likes=[]
        for i in self.liked_by.all():
            list_likes.append(i.id)
        return int(len(list_likes))

    def like_unlike_mod(self, otheruser):
        list_likes=[]
        for i in self.liked_by.all():
            list_likes.append(i.id)
        if otheruser.id in list_likes:
            (self.liked_by).remove(otheruser)
        else:
            (self.liked_by).add(otheruser)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "description": self.description,
            "date": self.date,
            "photo" : self.photo.url,
            "liked_by": [user.id for user in self.liked_by.all()],
            "comments" : [comment.id for comment in self.comments.all()]
        }


class Comment(models.Model):
    id          = models.AutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_owner', null=True)
    text        = models.CharField(max_length=280)
    liked_by    = models.ManyToManyField(User, related_name='comment_upvoter', blank=True)

    def __str__(self):
        return(f"{self.user}'s comment of id {self.id}")

    def get_number_likes (self):
        return len(int(self.liked_by))

    def like_unlike (self, otheruser):
        if otheruser in self.liked_by:
            (self.liked_by).remove(otheruser)
        else:
            (self.liked_by).append(otheruser)

    def serialize(self):
        return {
            "id" : self.id,
            "user" : self.user.username,
            "user_photo" : self.user.profile_photo.url,
            "text" : self.text,
            "liked_by" : [user.id for user in self.liked_by.all()]
        }

