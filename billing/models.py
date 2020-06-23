from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from accounts.models import GuestEmail
from django.urls import reverse
import stripe

stripe.api_key = "sk_test_uAMQwOWADa01RqYBsCucGkhF00rOxC8nDa"

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_ger(self, request):
        user = request.user
        created = False
        obj = None
        guest_email_id = request.session.get('guest_email_id')
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    customer_id = models.CharField(max_length=120, blank=True, null=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.create(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

    def get_change_payment_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None


class CardManager(models.Manager):
    def all(self):
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=card_response.id,
                brand=card_response.brand,
                country=card_response.country,
                exp_month=card_response.exp_month,
                exp_year=card_response.exp_year,
                last4=card_response.last4,
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    exp_month = models.IntegerField(blank=True, null=True)
    exp_year = models.IntegerField(blank=True, null=True)
    last4 = models.CharField(max_length=4, blank=True, null=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)


class ChargeManager(models.Manager):
    def create(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "no card"
        charge = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency="usd",
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id": order_obj.order_id},
        )
        new_charge_obj = self.model(
            billing_profile=billing_profile,
            stripe_id=charge.id,
            paid=charge.paid,
            refunded=charge.refunded,
            outcome=charge.outcome,
            outcome_type=charge.outcome.get('type'),
            seller_message=charge.outcome.get('seller_message'),
            risk_level=charge.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=True)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()


def billing_profile_update_default(sender, instance, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


pre_save.connect(billing_profile_update_default, sender=Card)


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
            email=instance.email
        )
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
