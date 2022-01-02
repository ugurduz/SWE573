from django.db import models
import uuid
from django.db.models.deletion import SET_NULL
from django.db.models.expressions import Value
from django.db.models.fields.related_descriptors import create_forward_many_to_many_manager
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

#USER MODELS

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length=20)
    interests = models.TextField(null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to='profilepictures/', default="/profilepictures/defaultProfile.png")
    credits = models.IntegerField(default=5, null=False, blank=False, validators=[MaxValueValidator(15), MinValueValidator(0)])
    userid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.user.username)

#@receiver(post_save, sender = Profiles)        
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profiles.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

def deleteUser(sender, instance, **kwargs): 
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender = User)
post_delete.connect(deleteUser, sender = Profiles)


#OFFER MODELS

class Offers(models.Model):
    
    OFFER_TYPE = (
            ('event','Offer'),
            ('gathering','Gathering')
    )

    EVENTSTATUS_TYPE = (
            ('done','Done'),
            ('canceled','Cancel'),
            ('inprogress','In Progress')
    )

    EXCHANGE_TYPE = (
            ('yes','yes'),
            ('no','no')
    )

    offerid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Profiles, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='images/', default="images/logo.png")
    hashtags = models.ManyToManyField('Tags', blank=True)
    #attendaceList = models.ManyToManyField('Attendants', blank=True)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    location = models.CharField(max_length=20)
    credits = models.IntegerField(default=0, null=False, blank=False, validators=[MaxValueValidator(15), MinValueValidator(0)])
    numberOfParticipants = models.IntegerField(default=0, null=False, blank=False)
    type = models.CharField(max_length=50, choices= OFFER_TYPE)
    eventstatus = models.CharField(max_length=50, choices= EVENTSTATUS_TYPE)
    exchange = models.CharField(max_length=50, choices= EXCHANGE_TYPE, default='no')

    #def save(credits):
     #   if type == "gathering":
      #      credits==0

    def __str__(self):
        return self.title


class Tags(models.Model):
    name = models.CharField(max_length=30)
    tagid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

class Feedbacks(models.Model):
    VOTE_TYPE = (
            ('up','Enjoyed'),
            ('down','Not Enjoyed')
    )
    owner = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices= VOTE_TYPE)
    voteid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    voteTotal = models.IntegerField(default=0, null=True, blank=True)
    voteRatio = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        unique_together = [['owner', 'offer']]

    def __str__(self):
        return self.offer.title

class Attendants(models.Model):
 
    APPROVAL_TYPE = (
            ('approval','Approval'),
            ('approved','Approve'),
            ('rejected','Reject')
    )

    OFFERSTATUS_TYPE = (
            ('done','Done'),
            ('canceled','Cancel'),
            ('inprogress','In Progress')
    )
    
    EXCHANGE_TYPE = (
            ('yes','yes'),
            ('no','no')
    )

    owner = models.ForeignKey(Profiles,  null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Offers, on_delete=models.CASCADE)
    requestid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices= APPROVAL_TYPE)
    offerstatus = models.CharField(max_length=50, choices= OFFERSTATUS_TYPE, default='inprogress')
    exchange = models.CharField(max_length=50, choices= EXCHANGE_TYPE, default='no')

    class Meta:
        unique_together = [['owner', 'event']]

    def __str__(self):
        return self.status

