from django.test.testcases import SimpleTestCase
from django.urls import reverse, resolve
from base.models import Offers, Profiles
from base.views import account, editaccount, events, event, profiles, register
from django.contrib.auth.models import User

class TestUrls(SimpleTestCase):
    def test_events_url_is_resolved(self):
        url=reverse('events')
        self.assertEquals(resolve(url).func, events)

    def test_register_url_is_resolved(self):
        url=reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_profiles_url_is_resolved(self):
        url=reverse('profiles')
        self.assertEquals(resolve(url).func, profiles)

    def test_account_url_is_resolved(self):
        url=reverse('account')
        self.assertEquals(resolve(url).func, account)

    def test_editaccount_url_is_resolved(self):
        url=reverse('editaccount')
        self.assertEquals(resolve(url).func, editaccount)

