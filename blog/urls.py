from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

app_name = "blog"
sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.PostList.as_view(), name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.PostDetail.as_view(),
        name="post_detail",
    ),
    path(
        "<int:post_id>/udostepnij-post/", views.SharePost.as_view(), name="share_post"
    ),
    path("kontakt/", views.ContactUs.as_view(), name="contact"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
