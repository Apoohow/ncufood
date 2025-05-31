"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('googleOauth.urls')),
    path('', include('restaurants.urls')),
    path('checkin/', include(('checkin.urls', 'checkin'), namespace='checkin')),
    path('article/', include(('article.urls', 'article'), namespace='article')),
    path('social/', include(('social.urls', 'social'), namespace='social')),
    path('food-analysis/', include(('food_analysis.urls', 'food_analysis'), namespace='food_analysis')),
    path('ai-assistant/', include(('ai_assistant.urls', 'ai_assistant'), namespace='ai_assistant')),
    path('ai-recommendation/', include(('ai_recommendation.urls', 'ai_recommendation'), namespace='ai_recommendation')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
