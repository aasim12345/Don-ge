from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task

def home(request):
    return render(request, 'main/index.html')
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'main/signup.html', {'form': form})


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Incorrect username or password.'

    return render(request, 'main/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date if due_date else None
            )

        return redirect('tasks')

    tasks = Task.objects.filter(user=request.user)

    return render(request, 'main/tasks.html', {
        'tasks': tasks
    })
@login_required
def complete_task(request, task_id):

    task = Task.objects.get(
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('tasks')


@login_required
def delete_task(request, task_id):

    task = Task.objects.get(
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect('tasks')
