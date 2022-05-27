from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from django.utils import timezone
from .models import Todo

def home(request):

    return render(request, 'todo/home.html')

# Create your views here.
def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        # Create user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')

            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {'form': UserCreationForm(), 'error': 'User name alredy taken'})

        else:
            return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': 'Password did not match'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form': AuthenticationForm, 'error': 'Username and password don\'t match'})
        else:
            login(request, user)
            return redirect('current_todos')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.created = timezone.now()
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.hmtl', {'form': TodoForm, 'error': 'Erro nos valores informados'})


def current_todos(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo/current_todos.html', {'todos': todos})


def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/view_todo.html', {'todo': todo, 'error': 'Valor não permitido'})


def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('current_todos')

