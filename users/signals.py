from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# sender = User, instance = instance of User, created = True or False
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            name=user.first_name,
            email=user.email,
            username=user.username
        )

        print("Profile created")


# sender = Profile, instance = instance of Profile, created = True or False
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user # profile.user
        user.delete()
        print("User deleted")
    except:
        pass


# create profile when user is created
post_save.connect(createProfile, sender=User)
# delete User when Profile is deleted
post_delete.connect(deleteUser, sender=Profile)

# @receiver(post_save, sender=User)
# def createProfile(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         Profile.objects.create(
#             user=user,
#             name = user.first_name,
#             email = user.email,
#             username = user.username
#             )
#         print("Profile created")
