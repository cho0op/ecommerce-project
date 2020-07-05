from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import MarketingPreferenceForm
from .models import MarketingPreference, Mailchimp
from .mixins import CsrfExemptMixin
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'marketing/base/forms.html'
    success_url = '/settings/email'
    success_message = "Marketing preference updated"

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login/?next=/settings/email')
        return super(MarketingPreferenceUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data()
        context['title'] = "Update marketing preference"
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


class MailchimpWebhookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get("data[email]")
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                subbed, mailchimp_subbed = (False, False)
            if subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exist():
                    qs.update(subscribed=subbed,
                              mailchimp_subscribed=mailchimp_subbed,
                              mailchimp_msg=str(data)
                              )
        return HttpResponse("Success", status=200)
# Create your views here.
