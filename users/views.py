from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """Завершает сеанс работы с приложением."""
    logout(request)
    return HttpResponseRedirect(reverse('animals:index'))


class RegisterView(View):
    form_class = UserCreationForm

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, 'users/register.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('animals:index'))
