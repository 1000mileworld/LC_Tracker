from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Problem

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from account.forms import RegistrationForm, AccountAuthenticationForm
from .forms import ProblemCreateForm, ProblemUpdateForm, GenerateProblemForm, ConfirmRedoForm

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect

import json
from django.core.serializers.json import DjangoJSONEncoder

from .func import gen_problems, shift_problems

def redo_view(request, pk):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    context = {}
    if request.method == 'POST':
        form = ConfirmRedoForm(request.POST, user=user, id=pk)
        if form.is_valid():
            if 'yes-redo' in request.POST:
                form.save(request.POST['rating'])
            return redirect('/')
    else:
        form = ConfirmRedoForm(user=user, id=pk)
    context['redo_form'] = form
    return render(request, 'base/confirm_redo.html', context)

def problem_list_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    context = {}
    context['problems'] = Problem.objects.filter(user=user)
    context['problems_json'] = json.dumps(list(context['problems'].values()), cls=DjangoJSONEncoder)
    context['easy_count'] = Problem.objects.filter(user=user, difficulty='Easy').count()
    context['medium_count'] = Problem.objects.filter(user=user, difficulty='Medium').count()
    context['hard_count'] = Problem.objects.filter(user=user, difficulty='Hard').count()
    context['total_count'] = context['easy_count']+context['medium_count']+context['hard_count']

    if request.method == 'POST':
        form = GenerateProblemForm(request.POST)
        if form.is_valid():
            if 'generate' in request.POST:
                num_problems = request.POST['num-problems']
                gen_problems(user, int(num_problems))
            elif 'shift' in request.POST:
                shift_problems(user)
            return redirect('/')

    return render(request, 'base/problem_list.html', context)

#switched to function view because it's easier to add a form to it
# class ProblemList(LoginRequiredMixin, ListView):
#     model = Problem
#     context_object_name = 'problems'

#     #restrict problem list view to user who created it
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['problems'] = context['problems'].filter(user=self.request.user)
#         context['problems_json'] = json.dumps(list(context['problems'].values()), cls=DjangoJSONEncoder)

#         return context

class ProblemDetail(LoginRequiredMixin, DetailView):
    model = Problem
    context_object_name = 'problem'

class ProblemCreate(LoginRequiredMixin, CreateView):
    #model, fields, success url specified in ProblemCreateForm
    template_name = 'base/problem_form.html'
    form_class = ProblemCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    #pass user back to form
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProblemCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

class ProblemUpdate(LoginRequiredMixin, UpdateView):    
    model = Problem
    form_class = ProblemUpdateForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProblemUpdate, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['id'] = self.kwargs['pk']
        return kwargs

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Problem
    context_object_name = 'problem'
    success_url = reverse_lazy('problems')
    
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

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
        form = AccountAuthenticationForm()
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
			form.save() #create account, then login below
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