from base.forms import OffersForm, FeedbackForm, StatusForm
import datetime
from django.test import TestCase

from base.models import Offers

class FormTest(TestCase):
    def test_offers_form_true(self):
        test_form =  {
        'title':'test event',
        'description':'desc',
        'picture':'images/logo.png', 
        'hashtags':'',
        'location':'london',
        'date':'2023-01-01',
        'time':'11:00',
        'credits':'0',
        'numberOfParticipants':'2',
        'type':'gathering',
        }
        form = OffersForm(data = test_form)
        self.assertTrue(form.is_valid())
    
    def test_feedback_form_false(self):
        test_form =  {
        'value':'neutral',
        'body':'Great event!',
        }
        form = FeedbackForm(data = test_form)
        self.assertFalse(form.is_valid())  
    
    def test_feedback_form_false(self):
        test_form =  {
        'value':'up',
        'body':'Great event!',
        }
        form = FeedbackForm(data = test_form)
        self.assertTrue(form.is_valid()) 