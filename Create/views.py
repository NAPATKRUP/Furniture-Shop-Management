from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Manage.models import Order, Order_Item, Stock, Item, Customer
from Account.models import Account

# Create your views here.
@login_required
@permission_required('Manage.add_order')
def create_order(request):
    return render(request, template_name='Create/create_order.html')


@login_required
@permission_required('Manage.add_order')
def send_order(request):
    if request.method == 'POST':
        cus_id = request.POST.get('cus-id')
        list_item = request.POST.get('list-item')
        items_value = request.POST.get('items-value')
        total_price = request.POST.get('total-price')

        list_item = list_item.split(",")
        list_item = list(map(int, list_item))
        items_value = items_value.split(",")
        items_value = list(map(int, items_value))
        total_price = float(total_price)

        fail_add = []
        complete_add = []
        total_price_now = 0

        #create order
        orders = Order.objects.create(
            account_id=Account.objects.get(user_id=request.user.id),
            cus_id=Customer.objects.get(id=cus_id),
            total_price=0
        )
        orders.save()

        for i in range(len(list_item)):
            stock = Stock.objects.get(pk=list_item[i])
            amount = stock.amount
            send_amount = items_value[i]

            #Check amount in DB
            if amount < send_amount:
                fail_add.append(send_amount-amount)
                complete_add.append(amount)
                send_amount = amount
            else:
                fail_add.append(0)
                complete_add.append(send_amount)

            # Update Stock
            stock.amount = amount - send_amount
            stock.save()

            # Create order item
            order_items = Order_Item.objects.create(
                    amount=send_amount,
                    color=stock.color,
                    price=stock.item_id.sale_price,
                    order_id=orders,
                    description=stock.item_id.description,
                    item_type=stock.item_id.item_type,
                    name=stock.item_id.name
                )
            order_items.save()

            total_price_now += stock.item_id.sale_price*send_amount

        orders.total_price = total_price_now
        orders.save()

        if (sum(fail_add)):
            send_status = {
                'complete_add': complete_add,
                'fail_add': fail_add,
                'total_price': total_price_now,
                'list_item': list_item,
                'items_value': items_value,
                'cus_id': cus_id,
                'order_id': orders.id
            }
            return show_status(request, send_status)
        else:
            return redirect('view_order', orders.id)

    return redirect('index')

@login_required
@permission_required('Manage.add_order')
def show_status(request, error_msg):
    context = {
        'error': [],
        'order_id': error_msg['order_id']
    }

    for i in range(len(error_msg['fail_add'])):
        if error_msg['fail_add'][i] != 0:
            txt_error = 'รายการ ' + Stock.objects.get(pk=error_msg['list_item'][i]).item_id.name + ' สามารถสั่งได้เพียง ' + str(error_msg['complete_add'][i]) + ' ชิ้น เนื่องจากรายการสินค้านี้มีจำนวนไม่พอ'
            context['error'].append(txt_error)

    return render(request, template_name='Create/show_status.html', context=context)