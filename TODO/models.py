from django.db import models
from django.utils import timezone


# from django.views.generic.edit import FormView
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login
# from django.views.generic.base import View
# from django.contrib.auth import logout


class Task(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=20)
    create_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


# class RegisterFormView(FormView):
#     form_class = UserCreationForm
#
#     # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
#     # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
#     success_url = "/login/"
#
#     # Шаблон, который будет использоваться при отображении представления.
#     template_name = "signup.html"
#
#     def form_valid(self, form):
#         # Создаём пользователя, если данные в форму были введены корректно.
#         form.save()
#
#         # Вызываем метод базового класса
#         return super(RegisterFormView, self).form_valid(form)
#
#
# class LoginFormView(FormView):
#     form_class = AuthenticationForm
#
#     # Аналогично регистрации, только используем шаблон аутентификации.
#     template_name = "logout.html"
#
#     # В случае успеха перенаправим на главную.
#     success_url = "/"
#
#     def form_valid(self, form):
#         # Получаем объект пользователя на основе введённых в форму данных.
#         self.user = form.get_user()
#
#         # Выполняем аутентификацию пользователя.
#         login(self.request, self.user)
#         return super(LoginFormView, self).form_valid(form)
#
# class LogoutView(View):
#     def get(self, request):
#         # Выполняем выход для пользователя, запросившего данное представление.
#         logout(request)
#
#         # После чего, перенаправляем пользователя на главную страницу.
#         return HttpResponseRedirect("/")


