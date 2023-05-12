"""house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from rental_app import views
from rental_app.views import homepage,product,signup,login,liked,profile,update_property,help_support,plans,pageNotFound,sell,terms_and_conditions,privacy_policy,admin_user

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage.homepage),
    path('<int:page_no>',homepage.homepage),
    path('product/', product.product),
    path('signup/',signup.signup),
    path('login/',login.login),
    path('product/<int:productID>',product.product),
    path('sell/',sell.sell),
    # path('success/',views.success,name='success'),
    path('liked/',liked.favour),
    path('profile/',profile.profile),
    path('update/<int:productID>',update_property.update_property),
    path('help_support/',help_support.help_support),
    # path('paymentGW/',payment_gateway.payment_gateway),
    path('plans/',plans.plans),
    # path('paymenthandler/', payment_gateway.paymenthandler, name='paymenthandler'),
    path('paymenthandler/', plans.paymenthandler, name='paymenthandler'),
    path('pageNotFound/',pageNotFound.pageNotFound),
    path('sell/images/',sell.images_files),
    path('terms&conditions/',terms_and_conditions.terms_And_conditons),
    path('privacy-policy',privacy_policy.privacy_policy),
    path('admin-user/',admin_user.admin_user),
    path('admin-user/upload',admin_user.admin_user_upload),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',views.homepage),
#     path('<int:page_no>',views.homepage),
#     path('product/', views.product),
#     path('signup/',views.signup),
#     path('login/',views.login),
#     path('product/<int:productID>',views.product),
#     path('sell/',views.sell),
#     path('success/',views.success,name='success'),
#     path('liked/',views.favour),
#     path('profile/',views.profile),
#     path('update/<int:productID>',views.update_property),
#     path('help_support/',views.help_support),

# ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


