from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateUserForm

# Create your views here.
class CreateUser(View):
    template_name = 'users/create_user.html'
    form_class = CreateUserForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        user = self.form_class(request.POST)
        if user.is_valid():
            user.save()
            return redirect('/user/login')
        else:
            return redirect('/user/create')


class LoginUser(View):
    template_name = 'users/login_user.html'

    def get(self, request):
        return render(request, self.template_name, {})