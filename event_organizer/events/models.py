from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Event(models.Model):

    CATEGORY_CHOICES = [
        ('music','Music'),
        ('tech','Technology'),
        ('sports','Sports'),
        ('cultural','Cultural'),
        ('workshop','Workshop'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200)

    image = models.ImageField(upload_to='events/', null=True, blank=True)

    category = models.CharField(
    max_length=20,
    choices=CATEGORY_CHOICES,
    default="music"
)

    max_participants = models.IntegerField()

    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    featured = models.BooleanField(default=False)

    def seats_left(self):
        return self.max_participants - self.registration_set.count()

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')


class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['joined_at']


class Profile(models.Model):

    ROLE_CHOICES = [
        ('student','Student'),
        ('organizer','Organizer')
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default="student")

    bio = models.TextField(blank=True)

    avatar = models.ImageField(upload_to='profiles/',null=True,blank=True)

    def __str__(self):
        return self.user.username
    

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):

        if created:
            Profile.objects.create(user=instance)
