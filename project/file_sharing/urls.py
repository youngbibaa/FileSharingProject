from django.urls import path
from .views import HomePageView, RegisterView, UserChangeView, ProfileView, CreateFileView, FileDetailView, download_file, view_download_history
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='file_sharing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_user/', UserChangeView.as_view(), name='change_user'),
    path('create_file/', CreateFileView.as_view(), name='create_file'),
    path('file_detail/<int:pk>', FileDetailView.as_view(), name='file_detail'),
    path('download/<int:pk>/', download_file, name='download_file'),
    path('download_history/', view_download_history, name="download_history")
]
