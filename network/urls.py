
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("index_following", views.index_following, name="index_following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # API Routes
    path("search", views.search, name="search"),
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("view_profile/<int:user_id>", views.view_profile, name="view_profile"),
    path("posts", views.new_post, name="new_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("edit_postP/<int:post_id>", views.edit_postP, name="edit_postP"),
    path("posts/<int:user_id>", views.get_feed, name="feed"),
    path("followers", views.get_followers_list, name="followers"),
    path("following", views.get_following_list, name="following"),
    path("post_view/<int:post_id>", views.view_post, name="post_view"),
    path("comment", views.commentP, name="make_comment"),
    path("view_comment/<int:comment_id>", views.comment_list, name="comment_view_det"),
    path("like_unlike/<int:post_id>/<int:logged_user_id>", views.like_unlike, name="like_unlike"),
    path("follow_user/<int:logged_user_id>/<int:another_user_id>", views.follow_user, name="follow_user"),
    path("get_followed/<int:another_user_id>/<int:logged_user_id>", views.get_followed, name="get_followed")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)