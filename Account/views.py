from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import Account, Owner, Employee


def my_login(request):
    context = {}

    if Owner.objects.all().count() == 0:
        return redirect('start')

    # Check already login
    if request.user.is_authenticated:
        return redirect('index')

    # Get detail in form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # Success
        if user:
            login(request, user)

            # Redirect
            next_url = request.POST.get('next_url')
            if next_url != '':
                return redirect(next_url)
            else:
                return redirect('index')

        # Fail
        else:
            context['username'] = username
            context['error'] = '* บัญชีผู้ใช้ หรือ รหัสผ่านผิด!'

    # Get url path
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='Account/login.html', context=context)


def let_start(request):
    context = {}

    if Owner.objects.all().count() > 0:
        return redirect('login')

    # Get detail in form
    if (request.method == 'POST'):
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        shop_name = request.POST.get('shop_name')

        context = {
            'fname': first_name,
            'lname': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'shop_name': shop_name
        }

        # Check already used
        if len(phone) != 10:
            context['error'] = '* กรุณากรอกเบอร์มือถือให้ถูกต้อง'
            return render(request, 'Account/start.html', context=context)
        elif '@' not in email or '.' not in email:
            context['error'] = '* กรุณากรอกอีเมลให้ถูกต้อง'
            return render(request, 'Account/start.html', context=context)
        elif password != password2:
            context['error'] = '* รหัสผ่านไม่ตรงกัน'
            return render(request, 'Account/start.html', context=context)

        # Add user to DB
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        account = Account(
            user=User.objects.get(username=username),
            phone=phone
        )
        account.save()

        # Add permission group
        try:
            Group.objects.get(name='Owner')
        except:
            g_o = Group.objects.create(name='Owner')
            l_o = [Permission.objects.get(name='Can add employee'), Permission.objects.get(name='Can change employee'),
                   Permission.objects.get(name='Can delete employee'), Permission.objects.get(
                       name='Can view employee'),
                   Permission.objects.get(name='Can add customer'), Permission.objects.get(
                       name='Can change customer'),
                   Permission.objects.get(name='Can delete customer'), Permission.objects.get(
                       name='Can view customer'),
                   Permission.objects.get(name='Can add supplier'), Permission.objects.get(
                       name='Can change supplier'),
                   Permission.objects.get(name='Can delete supplier'), Permission.objects.get(
                       name='Can view supplier'),
                   Permission.objects.get(name='Can add item'), Permission.objects.get(
                       name='Can change item'),
                   Permission.objects.get(name='Can delete item'), Permission.objects.get(
                       name='Can view item'),
                   Permission.objects.get(name='Can add stock'), Permission.objects.get(
                       name='Can change stock'),
                   Permission.objects.get(name='Can delete stock'), Permission.objects.get(
                       name='Can view stock'),
                   Permission.objects.get(name='Can add order'), Permission.objects.get(
                       name='Can change order'),
                   Permission.objects.get(name='Can delete order'), Permission.objects.get(
                       name='Can view order'),
                   Permission.objects.get(name='Can add order_ item'), Permission.objects.get(
                       name='Can change order_ item'),
                   Permission.objects.get(name='Can delete order_ item'), Permission.objects.get(name='Can view order_ item')]
            g_o.permissions.set(l_o)

        owner = Owner(
            account=Account.objects.get(
                user_id=User.objects.get(username=username)),
            shop_name=shop_name
        )
        owner.save()
        user.groups.add(Group.objects.get(name='Owner'))

        login(request, user)

        return redirect('index')

    return render(request, template_name='Account/start.html', context=context)


@login_required
def my_logout(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    user = request.user
    context = {}
    context['username'] = user.username

    # Get detail in form
    if request.method == 'POST':
        oldpass = request.POST.get('opass')
        newpass1 = request.POST.get('npass1')
        newpass2 = request.POST.get('npass2')

        check = authenticate(request, username=user.username, password=oldpass)

        # Check password matching
        if not check:
            context['error'] = '* รหัสผ่านเดิมไม่ถูกต้อง!'
            return render(request, template_name='Account/change_password.html', context=context)
        if newpass1 != newpass2:
            context['error'] = '* รหัสผ่านไม่ตรงกัน!'
            return render(request, template_name='Account/change_password.html', context=context)

        # Set password to DB
        user.set_password(newpass1)
        user.save()
        logout(request)
        return redirect('login')

    return render(request, template_name='Account/change_password.html', context=context)
