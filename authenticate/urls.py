from django.contrib import admin
from django.urls import path, include
from . import views

#django first looks for the file called settings.py from the ticketsystem then urls of ticksystem
#then it comes to url file inside the authenicate.url 
urlpatterns = [
    #views can call function too
    path('',views.homepage, name="homepage"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('ticket', views.ticket, name="ticket"),
    path('payment', views.payment, name="payment"),
    path('concert/<int:concert_id>/', views.concert_details, name='concert_details'),
    path('concert/<int:concert_id>/payment_post', views.payment_post, name='payment_post'),
    path('concert/<int:concert_id>/transaction_post', views.transaction_post, name='transaction_post'),
    path('concert/<int:concert_id>/success.html', views.success, name='success'),
    path('profile', views.profile, name="profile"),
]


