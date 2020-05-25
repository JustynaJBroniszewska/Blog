from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("udostepnij-post/", views.SharePost.as_view(), name="share_post"),
]
