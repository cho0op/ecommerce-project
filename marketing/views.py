from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin


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
# Create your views here.
