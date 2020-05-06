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
    
    path('profile/', views.Profile.as_view(), name="profile"),
    # GET for details PUT for update
    path('profile/<int:profile_id>/', views.Profile.as_view(), name="owner-profile"),
    
    path('signup/', views.Register.as_view(), name="signup"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    
    path('rentlist/', views.RentList.as_view(), name="rent-list"),
    path('rent/', views.Rent.as_view(), name="rent"),
    path('create/', views.ProductCreate.as_view(), name="create"),
    path('update/<int:product_id>/', views.ProductUpdate.as_view(), name='update'),
    path('return/<int:rentedItem_id>/', views.ReturnRent.as_view(), name='return'),
    path('delete/<int:product_id>/', views.ProductDelete.as_view(), name='delete'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)