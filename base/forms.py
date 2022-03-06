from django import forms
from .models import Problem

class ProblemCreateForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ('user',) #specifies what fields from the model not to include in the form.

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProblemCreateForm, self).__init__(*args, **kwargs)

    #restrict duplicates
    def clean_number(self):
        number = self.cleaned_data['number']
        if Problem.objects.filter(user=self.user, number=number).exists():
            raise forms.ValidationError("You have already added a problem with the same number.")
        return number

    def clean_title(self):
        title = self.cleaned_data['title']
        if Problem.objects.filter(user=self.user, title__iexact=title).exists(): #iexact means case insensitive
            raise forms.ValidationError("You have already added a problem with the same title.")
        return title

    def clean_url(self):
        url = self.cleaned_data['url']
        if Problem.objects.filter(user=self.user, url__iexact=url).exists():
            raise forms.ValidationError("You have already added a problem with the same title.")
        return url

class ProblemUpdateForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ('user',) #specifies what fields from the model not to include in the form.

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.id = kwargs.pop('id')
        super(ProblemUpdateForm, self).__init__(*args, **kwargs)

    #restrict duplicates when updating
    def clean_number(self):
        number = self.cleaned_data['number']
        if Problem.objects.filter(user=self.user, number=number).exists():
            if Problem.objects.filter(user=self.user, number=number).values('id')[0]['id']!=self.id:
                raise forms.ValidationError("Cannot update: problem with same number already exists.")
        return number

    def clean_title(self):
        title = self.cleaned_data['title']
        if Problem.objects.filter(user=self.user, title__iexact=title).exists(): #iexact means case insensitive
            if Problem.objects.filter(user=self.user, title__iexact=title).values('id')[0]['id']!=self.id:
                raise forms.ValidationError("Cannot update: problem with same title already exists.")
        return title

    def clean_url(self):
        url = self.cleaned_data['url']
        if Problem.objects.filter(user=self.user, url__iexact=url).exists():
            if Problem.objects.filter(user=self.user, url__iexact=url).values('id')[0]['id']!=self.id:
                raise forms.ValidationError("Cannot update: problem with same URL already exists.")
        return url