from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save


class MarketingPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    mailchimp_msg = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def make_marketing_pref_receiver(sender, instance, created, **kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)


def marketing_pref_update_receiver(sender, instance, created, **kwargs):
    if created:
        pass


post_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)
