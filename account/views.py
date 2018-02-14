from django.shortcuts import render, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView
from .forms import RegistrationForm

# Create your views here.
class RegisterView(CreateView):
    template_name = 'account/reg_form.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('inventory:data_list')
