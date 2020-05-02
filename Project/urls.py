"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from JarakAPI import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', views.ProductList.as_view(), name="products"),
    path('profile/', views.ProfileDetails.as_view(), name="profile"),
    path('profile/<int:profile_id>/', views.ProductOwnerProfile.as_view(), name="owner-profile"),
    path('signup/', views.Register.as_view(), name="signup"),
    path('login/', TokenObtainPairView.as_view(), name="login"),

    path('rent/', views.CreateRent.as_view(), name="rent"),
    path('rentlist/', views.RentList.as_view(), name="rent-list"),
    path('create/', views.Create.as_view(), name="create"),
    path('update/<int:product_id>/', views.Update.as_view(), name='update'),
    path('update_info/<int:profile_id>/', views.ProfileUpdate.as_view(), name='update-info'),
    path('delete/<int:product_id>/', views.Delete.as_view(), name='delete'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

