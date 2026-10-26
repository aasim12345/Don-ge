from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Task, Inventory
from django.db.models import Q
from django.utils import timezone


def home(request):

    # Show the original homepage before login
    if not request.user.is_authenticated:
        return render(request, 'main/index.html')

    # Get inventory belonging to this user
    items = Inventory.objects.filter(user=request.user)

    total_items = items.count()

    total_quantity = sum(
        item.quantity for item in items
    )

    total_value = sum(
        item.quantity * item.price for item in items
    )

    low_stock = items.filter(
        quantity__lte=5
    ).count()

    # Get upcoming and overdue tasks
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        completed=False,
        due_date__isnull=False
    ).order_by('due_date')[:5]

    # Send data to homepage
    context = {
        'total_items': total_items,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock': low_stock,
        'upcoming_tasks': upcoming_tasks,
        'today': timezone.localdate(),
    }

    return render(request, 'main/dashboard.html', context)
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
def inventory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        buy_link = request.POST.get('buy_link')

        if name:
            Inventory.objects.create(
                user=request.user,
                name=name,
                quantity=quantity,
                price=price,
                buy_link=buy_link
            )

        return redirect('inventory')

    items = Inventory.objects.filter(user=request.user)
  
    return render(request, 'main/inventory.html', {
        'items': items
    })


@login_required
def inventory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        buy_link = request.POST.get('buy_link', '')

        if name and quantity and price:
            Inventory.objects.create(
                user=request.user,
                name=name,
                quantity=quantity,
                price=price,
                buy_link=buy_link
            )

        return redirect('inventory')

    items = Inventory.objects.filter(user=request.user)

    total_items = items.count()
    total_quantity = sum(item.quantity for item in items)
    total_value = sum(item.quantity * item.price for item in items)
    low_stock = sum(1 for item in items if item.quantity <= 5)

     # Find low-stock items
    low_stock_items = items.filter(
    quantity__lte=5
    )

# Count stock warnings
    notification_count = low_stock_items.count()


    return render(request, 'main/inventory.html', {
        'items': items,
        'total_items': total_items,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock': low_stock,
        'low_stock_items': low_stock_items,
        'notification_count': notification_count,

    })


@login_required
def update_inventory(request, item_id):
    item = get_object_or_404(
        Inventory, id=item_id, user=request.user
    )

    if request.method == 'POST':
        quantity = request.POST.get('quantity')

        if quantity and quantity.isdigit():
            item.quantity = int(quantity)
            item.save()

    messages.success(
    request,
    "New inventory item added successfully!"
)
    
    messages.success(
    request,
    "Inventory stock updated successfully!"
)
    messages.success(
    request,
    "Inventory item deleted successfully!"
)
    return redirect('inventory')


@login_required
def delete_inventory(request, item_id):
    item = get_object_or_404(
        Inventory, id=item_id, user=request.user
    )

    if request.method == 'POST':
        item.delete()

    return redirect('inventory')
 


@login_required
def delete_inventory(request, item_id):
    item = get_object_or_404(
        Inventory,
        id=item_id,
        user=request.user
    )

    if request.method == 'POST':
        item.delete()

    return redirect('inventory')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == 'POST':
        task.delete()

    return redirect('tasks')


