from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (SignUpView, FeedbackViewSet, ProfileView,
                       TraineeQuizzesView, BlockProfileView, AdminListView,
                       GroupViewSet)

__all__ = ['urlpatterns']

router = DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet, basename='api_feedback')
router.register(r'permissions', GroupViewSet, basename='api_permissions')

urlpatterns = [
    path('token/', include([
        path('obtain/', TokenObtainPairView.as_view()),
        path('refresh/', TokenRefreshView.as_view()),
        ])),
    path('sign-up/', SignUpView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('admin_page/', AdminListView.as_view()),
    path('admin_page/<int:pk>', BlockProfileView.as_view()),
    path('trainee/', include([
        path('quizzes/', TraineeQuizzesView.as_view()),
        ])),
    ]

urlpatterns += router.urls
