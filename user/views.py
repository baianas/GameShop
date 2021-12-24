from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from user.forms import RegistrationForm

User = get_user_model()


class RegisterView(View):
    form_class = RegistrationForm
    template_name = 'user/registration.html'

    def get(self,request,*args,**kwargs):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})


    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('register-success'))
        return render(request,self.template_name,{'form':form})