from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from Manage.models import Customer, Supplier, Item, Stock
from Account.models import Account, Employee, Owner
from Manage.forms import addCustomerForm, addSupplierForm, addItemForm, addStockForm

#Employee View
@login_required
@permission_required('Account.change_employee')
def manage_employee(request):
    context = {'all_employee': []}
    employees = Employee.objects.all()
    for employee in employees:
        account = Account.objects.get(id=employee.account_id)
        user = User.objects.get(id=account.user_id)
        info = {
            'id': employee.id,
            'fname': user.first_name,
            'lname': user.last_name,
            'email': user.email,
            'phone': account.phone,
            'department': employee.get_department_display
        }
        context['all_employee'].append(info)

    return render(request, template_name='Manage/manage_employee.html', context=context)


@login_required
@permission_required('Account.add_employee')
def add_employee(request):
    context = {}
    # Get detail in form
    if (request.method == 'POST'):
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        acc_type = request.POST.get('type')

        context = {
            'fname': first_name,
            'lname': last_name,
            'email': email,
            'username': username,
            'phone': phone
        }

        # Check already used
        if (User.objects.filter(username=username).exists()):
            context['error'] = '* ชื่อผู้ใช้งานนี้ถูกใช้ไปแล้ว'
            return render(request, 'Add/add_employee.html', context=context)
        elif (User.objects.filter(email=email).exists()):
            context['error'] = '* อีเมลผู้ใช้งานนี้ถูกใช้ไปแล้ว'
            return render(request, 'Add/add_employee.html', context=context)
        elif '@' not in email or '.' not in email:
            context['error'] = '* กรุณากรอกอีเมลให้ถูกต้อง'
            return render(request, 'Add/add_employee.html', context=context)
        elif len(phone) != 10:
            context['error'] = '* กรุณากรอกเบอร์มือถือให้ถูกต้อง'
            return render(request, 'Add/add_employee.html', context=context)
        elif password != password2:
            context['error'] = '* รหัสผ่านไม่ตรงกัน'
            return render(request, 'Add/add_employee.html', context=context)

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

        employee = Employee(
            account=Account.objects.get(
                user_id=User.objects.get(username=username)),
            owner_id=Owner.objects.get(
                account_id=Account.objects.get(user_id=request.user.id))
        )

        if acc_type == 'po':
            #Add permission group
            try:
                Group.objects.get(name='Purchasing_Officer')
            except:
                g_po = Group.objects.create(name='Purchasing_Officer')
                l_po = [Permission.objects.get(name='Can add supplier'), Permission.objects.get(name='Can change supplier'), 
                    Permission.objects.get(name='Can delete supplier'), Permission.objects.get(name='Can view supplier'), 
                    Permission.objects.get(name='Can add item'), Permission.objects.get(name='Can change item'), 
                    Permission.objects.get(name='Can delete item'), Permission.objects.get(name='Can view item'), 
                    Permission.objects.get(name='Can add stock'), Permission.objects.get(name='Can change stock'), 
                    Permission.objects.get(name='Can delete stock'), Permission.objects.get(name='Can view stock')]
                g_po.permissions.set(l_po)

            employee.department = 'PURCHASING_OFFICER'
            user.groups.add(Group.objects.get(name='Purchasing_Officer'))

        elif acc_type == 'so':
            #Add permission group
            try:
                Group.objects.get(name='Sale_Officer')
            except:
                g_so = Group.objects.create(name='Sale_Officer')
                l_so = [Permission.objects.get(name='Can add customer'), Permission.objects.get(name='Can change customer'), 
                    Permission.objects.get(name='Can delete customer'), Permission.objects.get(name='Can view customer'), 
                    Permission.objects.get(name='Can view stock'), 
                    Permission.objects.get(name='Can add order'), Permission.objects.get(name='Can change order'), 
                    Permission.objects.get(name='Can delete order'), Permission.objects.get(name='Can view order'), 
                    Permission.objects.get(name='Can add order_ item'), Permission.objects.get(name='Can change order_ item'), 
                    Permission.objects.get(name='Can delete order_ item'), Permission.objects.get(name='Can view order_ item')]
                g_so.permissions.set(l_so)

            employee.department = 'SALE_OFFICER'
            user.groups.add(Group.objects.get(name='Sale_Officer'))
        employee.save()

        return redirect('manage_employee')

    return render(request, template_name='Add/add_employee.html', context=context)


@login_required
@permission_required('Account.change_employee')
def edit_employee(request, id):
    context = {}
    context['id'] = id
    return render(request, template_name='Edit/edit_employee.html', context=context)


#Customer View
@login_required
@permission_required('Manage.change_customer')
def manage_customer(request):
    context = {'all_customer': []}
    customers = Customer.objects.all()
    for customer in customers:
        info = {
            'id': customer.id,
            'fname': customer.fname,
            'lname': customer.lname,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address
        }
        context['all_customer'].append(info)

    return render(request, template_name='Manage/manage_customer.html', context=context)


@login_required
@permission_required('Manage.add_customer')
def add_customer(request):
    context = {}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user_id = request.user.id
        account = Account.objects.get(user_id=user_id)
        form = addCustomerForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.create(
                fname=fname,
                lname=lname,
                email=email,
                phone=phone,
                address=address,
                account_id=account
            )
            return redirect('manage_customer')
        else:
            context['form'] = form

    elif request.method == 'GET':
        form = addCustomerForm()
        context['form'] = form

    return render(request, template_name='Add/add_customer.html', context=context)


@login_required
@permission_required('Manage.change_customer')
def edit_customer(request, id):
    context = {}
    context['id'] = id
    return render(request, template_name='Edit/edit_customer.html', context=context)


#Supplier View
@login_required
@permission_required('Manage.change_supplier')
def manage_supplier(request):
    context = {'all_supplier': []}
    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        info = {
            'id': supplier.id,
            'name': supplier.name,
            'address': supplier.address,
            'email': supplier.email,
            'phone': supplier.phone
        }
        context['all_supplier'].append(info)

    return render(request, template_name='Manage/manage_supplier.html', context=context)


@login_required
@permission_required('Manage.add_supplier')
def add_supplier(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user_id = request.user.id
        account = Account.objects.get(user_id=user_id)
        form = addSupplierForm(request.POST)
        if form.is_valid():
            supplier = Supplier.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                account_id=account
            )
            return redirect('manage_supplier')
        else:
            context['form'] = form

    elif request.method == 'GET':
        form = addSupplierForm()
        context['form'] = form

    return render(request, template_name='Add/add_supplier.html', context={'form': form})


@login_required
@permission_required('Manage.change_supplier')
def edit_supplier(request, id):
    context = {}
    context['id'] = id
    return render(request, template_name='Edit/edit_supplier.html', context=context)


#Item View
@login_required
@permission_required('Manage.change_item')
def manage_item(request):
    context = {'all_item': []}
    items = Item.objects.all()
    for item in items:
        info = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'item_type': item.item_type,
            'purchase_price': item.purchase_price,
            'sale_price': item.sale_price,
            'supplier_name': item.supplier_id.name
        }
        context['all_item'].append(info)

    return render(request, template_name='Manage/manage_item.html', context=context)


@login_required
@permission_required('Manage.add_item')
def add_item(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        item_type = request.POST.get('item_type')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')
        try:
            supplier_id = request.POST.get('supplier_id')
            supplier = Supplier.objects.get(pk=supplier_id)
        except:
            pass
        form = addItemForm(request.POST)
        if form.is_valid():
            item = Item.objects.create(
                name=name,
                description=description,
                item_type=item_type,
                purchase_price=purchase_price,
                sale_price=sale_price,
                supplier_id=supplier
            )
            return redirect('manage_item')
        else:
            context['form'] = form

    elif request.method == 'GET':
        form = addItemForm()
        context['form'] = form

    return render(request, template_name='Add/add_item.html', context={'form': form})


@login_required
@permission_required('Manage.change_item')
def edit_item(request, id):
    context = {}
    context['id'] = id
    return render(request, template_name='Edit/edit_item.html', context=context)


#Stock View
@login_required
@permission_required('Manage.change_stock')
def manage_stock(request):
    context = {'all_stock': []}
    stocks = Stock.objects.all()
    for stock in stocks:
        info = {
            'id': stock.id,
            'color': stock.color,
            'amount': stock.amount,
            'item_id': stock.item_id.id
        }
        context['all_stock'].append(info)

    return render(request, template_name='Manage/manage_stock.html', context=context)


@login_required
@permission_required('Manage.add_stock')
def add_stock(request):
    context = {}
    if request.method == 'POST':
        color = request.POST.get('color')
        amount = request.POST.get('amount')
        try:
            item_id = request.POST.get('item_id')
            item = Item.objects.get(pk=item_id)
        except:
            pass
        form = addStockForm(request.POST)
        if form.is_valid():
            stock = Stock.objects.create(
                item_id=item,
                color=color,
                amount=amount
            )
            return redirect('manage_stock')
        else:
            context['form'] = form

    elif request.method == 'GET':
        form = addStockForm()
        context['form'] = form

    return render(request, template_name='Add/add_stock.html', context={'form': form})


@login_required
@permission_required('Manage.change_stock')
def edit_stock(request, id):
    context = {}
    context['id'] = id
    return render(request, template_name='Edit/edit_stock.html', context=context)
