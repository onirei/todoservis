from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Task
from .forms import ChangeTask, SignUpForm, LoginForm

from django.contrib.auth import login, logout, authenticate

import pandas as pd
import numpy as np
import io
import matplotlib as mpl
import matplotlib.pyplot as plt



# Create your views here.

# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

def task_list(request):
    if request.user.is_authenticated:
        tasks1 = Task.objects.filter(create_date__lte=timezone.now()).order_by('create_date').filter(author=request.user).filter(status='не завершено')
        tasks2 = Task.objects.filter(create_date__lte=timezone.now()).order_by('create_date').filter(author=request.user).filter(status='выполнено')
        tasks3 = Task.objects.filter(create_date__lte=timezone.now()).order_by('create_date').filter(author=request.user).filter(status='провалено')
        return render(request, 'TODO/index.html', {'tasks1': tasks1, 'tasks2': tasks2, 'tasks3': tasks3})
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
        df = pd.DataFrame(list(Task.objects.all().filter(author=request.user).values_list()),
                          columns=['id', 'author', 'title', 'text', 'status', 'priority', 'create_date',
                                   'expiration_date']).set_index(['id'])
        # df.to_csv('TODO/data.csv')

        # stata = Task.objects.filter(create_date__lte=timezone.now()).order_by('-create_date').filter(author=request.user)
        data = 'sdfgh'


        # df['expiration_date'] = pd.to_datetime(df['expiration_date']).dt.tz_convert('Europe/Moscow')
        # data = df
        # ts_utc = df.tz_convert("UTC")
        # ts_utc.index.tz = None

        # data = df['create_date'].values
        # data = [data[3],data[1],data[3] - data[1]]
        # data = pd.to_datetime(data[3] - data[1])
        # data = df[(df.expiration_date == data[3])]
        data = []
        for index, row in df.iterrows():
            data.append(row['expiration_date'] - row['create_date'])

        data = np.mean(data)





        # df['expiration_date'] = pd.to_datetime(df['expiration_date'])
        dates = df['expiration_date'].values
        a = []
        b = []
        c = []
        for _ in dates:
            _df = df[(df.expiration_date <= _)]
            a.append(_df['status'][(_df.status == 'не завершено')].count())
            b.append(_df['status'][(_df.status == 'выполнено')].count())
            c.append(_df['status'][(_df.status == 'провалено')].count())
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(1000 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 10})
        plt.title('RU New Domain Names Registration')
        plt.xlabel('Время')
        plt.ylabel('Количество')
        ax = plt.axes()
        ax.yaxis.grid(True)
        plt.plot(dates, a, linestyle='solid', label='не завершено')
        plt.plot(dates, b, linestyle='solid', label='выполнено')
        plt.plot(dates, c, linestyle='solid', label='провалено')
        plt.legend(loc='upper left', frameon=False)
        fig.savefig('TODO/static/img/domains.png')

        data_names = ['выполнено', 'провалено']
        data_values = [df['status'][(df.priority == 'низкий')].count(),
                       df['status'][(df.priority == 'обычный')].count()]
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(400 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})
        plt.title('Диаграмма соотношения успешных задач к проваленным (%)')
        plt.pie(
            data_values, autopct='%1.2f%%', radius=1.1,
            explode=[0.05] + [0 for _ in range(len(data_names) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='upper center', labels=data_names)
        fig.savefig('TODO/static/img/pie2.png')

        data_names = ['низкий', 'обычный', 'высокий']
        data_values = [df['priority'][(df.priority == 'низкий')].count(),
                       df['priority'][(df.priority == 'обычный')].count(),
                       df['priority'][(df.priority == 'высокий')].count()]
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(400 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})
        plt.title('Диаграмма приоритетов задач (%)')
        # xs = range(len(data_names))
        plt.pie(
            data_values, autopct='%1.2f%%', radius=1.1,
            explode=[0.02, 0.02, 0.02])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower center', labels=data_names)
        fig.savefig('TODO/static/img/pie.png')

        """
        добавить среднее время выполнения задания, только выполненых
        соотношение успешных к проваленным, можно диаграммой (процент успеха)
        всего активных заданий, выполненых, проваленных
        
        """

        stata = [a[-1], b[-1], c[-1]]

        return render(request, 'TODO/statistic.html', {'stata': stata,'data': data})
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
    return HttpResponseRedirect( '/')
