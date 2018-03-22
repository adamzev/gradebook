from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


# TODO Hide password requirements until they are violated
'''
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/sign_up.html'
'''


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect("/dashboard/")

        messages.warning(request, "Form is invalid")
        view_data = {
            'form': form,
        }

        return  render(request, 'registration/sign_up.html', view_data)

    else:
        form = UserCreationForm()
        view_data = {
            'form': form,
        }

        return  render(request, 'registration/sign_up.html', view_data)
