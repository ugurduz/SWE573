from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from base.models import Offers
from base.views import createevent
import datetime

class Offers_model_test(TestCase):              
    @classmethod

    def setUp(self):
        self.testu = User.objects.create(username='testuser')
        self.testuser = self.testu.profiles

    def testOffer(self):
        offer = Offers(
            created=timezone.now(),
            owner=self.testuser,
            title = "Test" , 
            description="desc",
            picture="images/logo.png", 
            date='2023-01-01',
            time='11:00',
            location = 'london',
            credits=1,
            numberOfParticipants=1,
            type='event',
            eventstatus='inprogress',
            exchange = 'yes'
            )
        self.assertEqual(offer.owner, self.testuser)
        self.assertEqual(offer.title, "Test")