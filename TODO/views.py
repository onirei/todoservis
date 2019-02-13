from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Task
from .forms import ChangeTask, SignUpForm, LoginForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(create_date__lte=timezone.now()).order_by('-create_date').filter(author=request.user)
        return render(request, 'TODO/index.html', {'tasks': tasks})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                my_password = form.cleaned_data['password']
                user = authenticate(username=username, password=my_password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('/')
        else:
            form = LoginForm()
        return render(request, 'TODO/index.html', {'form': form})
    # if request.method == 'POST':
    #     form = AuthenticationForm(request.POST)
    #     if form.is_valid():
    #         username = request.POST['username']
    #         my_password = request.POST['password']
    #         user = authenticate(username=username, password=my_password)
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #         return redirect('/')
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'TODO/index.html', {'form': form})



    # # username = None
    # if request.user.is_authenticated:
    #     # username = request.user.username
    #     tasks = Task.objects.filter(expiration_date=timezone.now()).order_by('expiration_date')
    #     return render(request, 'TODO/index.html', {'tasks': tasks})
    # else:
    #     tasks = Task.objects.filter(expiration_date=timezone.now()).order_by('expiration_date')
    #     return render(request, 'TODO/index.html', {'tasks': tasks})

def change(request):
    if request.user.is_authenticated:
        if request.POST:
            add_form = ChangeTask(request.POST)
            chn_form = ChangeTask(request.POST)
            if add_form.is_valid() and '_add' in request.POST:
                author = request.user
                title = add_form.cleaned_data['title_field']
                text = add_form.cleaned_data['text_field']
                status = add_form.cleaned_data['status']
                priority = add_form.cleaned_data['priority']
                create_date = add_form.cleaned_data['create_date']
                expiration_date = add_form.cleaned_data['expiration_date']
                task_obj = Task(author=author, title=title, status=status, priority=priority, text=text,
                                create_date=create_date, expiration_date=expiration_date)
                task_obj.save()
                return HttpResponseRedirect('/')
            elif chn_form.is_valid() and '_del' in request.POST:
                task_obj = Task.objects.get(id=chn_form.cleaned_data['id_field'])
                task_obj.delete()
                return HttpResponseRedirect('/')
            elif chn_form.is_valid() and '_chn' in request.POST:
                task_obj = Task.objects.get(id=chn_form.cleaned_data['id_field'])
                task_obj.title = chn_form.cleaned_data['title_field']
                task_obj.text = chn_form.cleaned_data['text_field']
                task_obj.status = chn_form.cleaned_data['status']
                task_obj.priority = chn_form.cleaned_data['priority']
                task_obj.create_date = chn_form.cleaned_data['create_date']
                task_obj.expiration_date = chn_form.cleaned_data['expiration_date']
                task_obj.save()
                return HttpResponseRedirect('/')
        else:
            add_form = ChangeTask()
            tasks = Task.objects.filter(create_date__lte=timezone.now()).order_by('-create_date').filter(
                author=request.user)
            chn_form = ()
            for task in tasks:
                chn_form += (ChangeTask(initial={'id_field': task.id, 'title_field': task.title, 'text_field': task.text,
                                              'status': task.status, 'priority': task.priority,
                                              'create_date': task.create_date,
                                              'expiration_date': task.expiration_date}),)

        return render(request, 'TODO/change.html', {'add_form': add_form, 'chn_form': chn_form})
    else:
        return HttpResponseRedirect('/')





def statistic(request):
    if request.user.is_authenticated:
        pass
        return render(request, 'TODO/statistic.html')
    else:
        return HttpResponseRedirect('/')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=my_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'TODO/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'TODO/index.html', {})
