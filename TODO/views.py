from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import Task
from .forms import ChangeTask, SignUpForm, LoginForm
from django.contrib.auth import login, logout, authenticate
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def task_list(request):
    #вывод в три колонки по пользователю если авторизован
    if request.user.is_authenticated:
        tasks1 = Task.objects.filter(create_date__lte=timezone.now()).order_by('create_date').filter(author=request.user).filter(status='не завершено')
        tasks2 = Task.objects.filter(create_date__lte=timezone.now()).order_by('create_date').filter(author=request.user).filter(status='выполнено')
        tasks3 = Task.objects.filter(create_date__lte=timezone.now()).order_by('create_date').filter(author=request.user).filter(status='провалено')
        return render(request, 'TODO/index.html', {'tasks1': tasks1, 'tasks2': tasks2, 'tasks3': tasks3})
    # форма входа
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


def change(request):
    if request.user.is_authenticated:
        if request.POST:
            add_form = ChangeTask(request.POST)
            chn_form = ChangeTask(request.POST)
            # добавление новой записи
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
            #удаление записи
            elif chn_form.is_valid() and '_del' in request.POST:
                task_obj = Task.objects.get(id=chn_form.cleaned_data['id_field'])
                task_obj.delete()
                return HttpResponseRedirect('/')
            #редактирование существующей
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
            #получаем все записи пользователя
            tasks = Task.objects.filter(create_date__lte=timezone.now()).order_by('-create_date').filter(
                author=request.user)
            chn_form = ()
            #создаём массив форм с данными поумолчанию для редактирования, хотя стоило бы использовать фабрику форм
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
        #для отладки датафрейм
        # df.to_csv('TODO/data.csv')

        #подсчёт среднего времени на задачу
        data = []
        for index, row in df.iterrows():
            data.append(row['expiration_date'] - row['create_date'])

        data = np.mean(data)

        #линейный график задач
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

        #диаграмма соотношения выполненых задак к проваленным
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

        #диаграмма соотношения задач по приоритету
        data_names = ['низкий', 'обычный', 'высокий']
        data_values = [df['priority'][(df.priority == 'низкий')].count(),
                       df['priority'][(df.priority == 'обычный')].count(),
                       df['priority'][(df.priority == 'высокий')].count()]
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(400 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})
        plt.title('Диаграмма приоритетов задач (%)')
        plt.pie(
            data_values, autopct='%1.2f%%', radius=1.1,
            explode=[0.02, 0.02, 0.02])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower center', labels=data_names)
        fig.savefig('TODO/static/img/pie.png')

        #подсчёт кол-ва задач по статусу, в отрисовке графика последние значения как раз это и показывали
        stata = [a[-1], b[-1], c[-1]]

        return render(request, 'TODO/statistic.html', {'stata': stata,'data': data})
    else:
        return HttpResponseRedirect('/')


#регистрация прользователя и логирование
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

# выход
def logout_view(request):
    logout(request)
    return HttpResponseRedirect( '/')
