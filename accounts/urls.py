from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.hmac.views import RegistrationView
from accounts.forms import FamoUserForm
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    # url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^register/$', RegistrationView.as_view(form_class=FamoUserForm), name='registration_register'),
    # url(r'^$', include('registration.backends.hmac.urls')),
]
