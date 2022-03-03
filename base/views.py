from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Problem

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from account.forms import RegistrationForm, AccountAuthenticationForm
from django.http import HttpResponse

from django.contrib.auth import login, authenticate

class ProblemList(LoginRequiredMixin, ListView):
    model = Problem
    context_object_name = 'problems'

    #restrict problem list view to user who created it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = context['problems'].filter(user=self.request.user)
        return context

class ProblemCreate(LoginRequiredMixin, CreateView):
    model = Problem
    #fields = '__all__' #keyword, list all items
    fields = ['number','title']
    success_url = reverse_lazy('problems') #redirect on successful create

    #overwrite default method
    #force create task user to be the logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProblemCreate, self).form_valid(form)
    
def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('problems')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                return redirect('problems')
    else:
        form = AccountAuthenticationForm
    context['login_form'] = form
    return render(request, "account/login.html", context)

def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return redirect('problems')

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save() #creat account, then login below
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('problems')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)