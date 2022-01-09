from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('signin/', views.signin, name="signin"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('profiles/', views.profiles, name="profiles"),
    path('activity/', views.activity, name="activity"),
    path('createevent/', views.createevent, name="createevent"),
    path('updateevent/<str:pk>/', views.updateevent, name="updateevent"),
    path('deleteevent/<str:pk>/', views.deleteevent, name="deleteevent"),
    path('feedback/<str:pk>/', views.feedback, name="feedback"),
    path('', views.events, name="events"),
    path('event/<str:pk>/', views.event, name="event"),
    path('event/<str:pk>/<str:sk>', views.approve, name="approve"),
    path('exchange/<str:pk>/<str:sk>', views.creditexchange, name="exchange"),
    path('gatherings/', views.gatherings, name="gatherings"),
    path('creategathering/', views.creategathering, name="creategathering"),
    path('', views.loginUser, name="login_register"),
    path('login_register/', views.loginUser, name="login_register"),
    path('account/', views.account, name="account"),
    path('editaccount/', views.editaccount, name="editaccount"),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)