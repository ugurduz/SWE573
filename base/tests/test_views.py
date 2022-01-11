    
from django.test.testcases import SimpleTestCase, TransactionTestCase
from django.urls import reverse, resolve
from base.models import Offers, Profiles
from base.views import events, event, profiles, register
from django.contrib.auth.models import User

class TestViews(TransactionTestCase):    

    def test_event_view(self):
        test_user = User.objects.create_user(username='testuser', password='Ax-2345*aa')
        test_user.save()

        test_service = Offers.objects.create(
            owner = test_user.profiles,
            title = "Test Offer",
            description = "test",    
            picture = "images/logo.png",
            date = '2023-01-01',
            time = '11:00',
            location = "london",
            credits = 1,
            numberOfParticipants = 1,
            type = "event",
            eventstatus = "inprogress",
            exchange = 'no'
        )

        test_service.save()

        event=Offers.objects.get(owner=test_user.profiles)
        self.assertEqual(event.title, "Test Offer")

    def test_offer_update_view(self):
        test_user = User.objects.create_user(username='testuser2', password='Ax-2345*aa')
        test_user.save()

        test_service = Offers.objects.create(
            owner = test_user.profiles,
            title = "Test Offer2",
            description = "test",    
            picture = "images/logo.png",
            date = '2023-01-01',
            time = '11:00',
            location = "london",
            credits = 1,
            numberOfParticipants = 1,
            type = "event",
            eventstatus = "inprogress",
            exchange = 'no'
        )

        event=Offers.objects.get(title="Test Offer2")
        event.title="Test Offer Updated"
        test_service.title=event.title
        test_service.save()
        self.assertEqual(test_service.title, "Test Offer Updated")
