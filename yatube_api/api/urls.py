from rest_framework.routers import SimpleRouter

from django.urls import include, path

from yatube_api.urls import API_VERSION
from .views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet

router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='followers')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path(f'{API_VERSION}/', include(router.urls)),
    path(f'{API_VERSION}/', include('djoser.urls.jwt')),
]
