from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here.
from django.utils.text import slugify


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    Searching_Name = models.CharField(max_length=50)
    interests = (
        ("Technology", "Technology"),
        ("handmade", "handmade"),
        ("software development", "software development"),
        ("Cars", "Cars"),
        ("Business", "Business"),
        ("Freelancing", "Freelancing"),
        ("Animals", "Animals")
    )
    interest = models.CharField(choices=interests, max_length=50)
    date = models.DateTimeField(auto_now=True)

    pending = models.ManyToManyField('profile', blank=True)
    friends = models.ManyToManyField('profile', related_name='users_friends', blank=True)
    chatters = models.ManyToManyField('profile', related_name='chats', blank=True)
    online = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = str(self.user)
        super(profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    @receiver(user_logged_in)
    def got_online(sender, user, request, **kwargs):
        user.profile.online = True
        user.profile.save()

    @receiver(user_logged_out)
    def got_offline(sender, user, request, **kwargs):
        user.profile.online = False
        user.profile.save()

    class Meta:
        ordering = ["-date"]


class message(models.Model):

    Sender = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='Sender', null=True, blank=True)
    receiver = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    message = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to="Chatting images", null=True, blank=True)
    file = models.FileField(upload_to="Chatting files", null=True, blank=True,  storage=RawMediaCloudinaryStorage())
    read = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    Date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('message', on_delete=models.CASCADE, related_name="replied_msg", null=True, blank=True)

    def __str__(self):
        return str(self.message)

    class Meta:
        ordering = ['Date']


class Notification(models.Model):
    reciever = models.ForeignKey(profile, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='sender', blank=True, null=True)
    read = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)

    class Meta:
        ordering = ['-date']


class Group(models.Model):
    admin = models.ForeignKey(profile, related_name="group_admin", on_delete=models.CASCADE)
    members = models.ManyToManyField(profile, blank=True)
    group_name = models.CharField(max_length=100, unique=True)
    group_image = models.ImageField(upload_to='groups_images', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    topics = (
        ("Technology", "Technology"),
        ("handmade", "handmade"),
        ("software development", "software development"),
        ("Cars", "Cars"),
        ("Business", "Business"),
        ("Freelancing", "Freelancing"),
        ("Animals", "Animals")
    )

    topic = models.CharField(choices=topics, max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.group_name)

    class Meta:
        ordering = ["-date"]


class group_message(models.Model):
    sender = models.ForeignKey(profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="Chatting images", null=True, blank=True)
    file = models.FileField(upload_to="Chatting files", null=True, blank=True,  storage=RawMediaCloudinaryStorage())
    readers = models.ManyToManyField(profile, related_name="readers", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey("group_message", related_name="g_msgs", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.message)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
