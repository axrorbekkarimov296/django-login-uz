from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        login_data = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, login=login_data, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_page')  # Foydalanuvchi sahifasiga o'tkazish
        else:
            return render(request, 'registration/login.html', {'error': 'Login yoki parol xato!'})
    return render(request, 'registration/login.html')


def register_view(request):
    if request.method == 'POST':
        login = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']

        # Parollar to'g'ri kirilganligini tekshiramiz
        if password1 != password2:
            return render(request, 'registration/register.html', {'error': 'Parollar bir biriga mos kelmayapti!'})

        # Foydalanuvchini yaratamiz
        try:
            CustomUser.objects.create_user(
                login=login,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )
            return redirect('login')  # Login - tizimga kiring sahifasiga o'tkazish
        except Exception as e:
            # Foydalanuvchi yaratishda xatolik
            return render(request, 'registration/register.html', {'error': str(e)})
    return render(request, 'registration/register.html')


@login_required
def user_page(request):
    return render(request, 'user_page.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('login')
