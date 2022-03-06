from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

# Create your views here.
from accounts.auth import learner_only
from materials.filters import CourseFilter, CatFilter
from materials.models import Categories, Courses, Order
from .forms import CommentForm
from .models import *
from django.http import JsonResponse
import json
import datetime
import os
from django.db import connection

@learner_only
def home(request):
    category=Categories.objects.all().order_by('-id')

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {
        'category_material': category,
        'activate_home': 'active',

        'items': items,
        'order': order,
        'cartItems': cartItems,
    }


    return render(request, 'materials/content.html', context )

# for courses in course page
@learner_only
def course(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping': False}
        cartItems = order['get_cart_items']

    courses=Courses.objects.all().order_by('course_Name')
    courses_filter = CourseFilter(request.GET, queryset=courses)
    courses_final = courses_filter.qs

    context={
        'course_material':courses_final,
        'user_course_filter':courses_filter,
        'activate_courses':'active',
        'cartItems': cartItems,
        'items': items,
        'order': order,
        # cartItems=order['get_cart_items']
    }

    return render(request, 'materials/courses.html', context )

#retrieving course according to category
@learner_only
def get_course_category(request,categories_id):
    category=Categories.objects.get(id=categories_id)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping': False}
        cartItems = order['get_cart_items']
    context={
        'category':category,
        'cartItems': cartItems,
        'items': items,
        'order': order,
        'activate_home': 'active',
    }
    return render(request,'materials/get_course_category.html',context)

# recently
def details(request,i_id):
    courseDetail = Courses.objects.get(id=i_id)
    comments = Comments.objects.filter(course_id=i_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comments.objects.create(course_id=i_id, user=request.user, content=content)
            comment.save()

    else:
        comment_form = CommentForm()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping': False}
        cartItems = order['get_cart_items']
    files=Courses.objects.get(id=i_id)

    context={
        'i':files,
        'activate_courses': 'active',
        'cartItems': cartItems,
        'items': items,
        'order': order,
        'course': courseDetail,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'materials/details.html', context)




def cart(request):
    if request.user.is_authenticated:
        customer=request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping': False}
        cartItems = order['get_cart_items']

    context={'items':items,
             'order':order,
             'cartItems':cartItems}
    return render(request,'materials/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context={'items':items ,
             'order':order,
             'cartItems':cartItems}
    return render(request,'materials/checkout.html',context)



def updateItem(request):
    data=json.loads(request.body)
    iId=data['iId']
    action = data['action']

    print('Action:',action)
    print('iId:',iId)

    customer = request.user
    i=Courses.objects.get(id=iId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order, product=i)

    if action =='add':
        orderItem.quantity=(orderItem.quantity +1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()



    return JsonResponse('item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )


    else:
        print('user not logged in')
    return JsonResponse('Payment complete',safe=False)




def orderhistory(request):
    userid = request.user.id
    cursor=connection.cursor()
    cursor.execute("""SELECT dzz.id, dop.quantity,dxx.address,dxx.city,dmf.course_Name,dmf.price,dmf.course_Image,
case dzz.complete
        when 1 then 'completed'
        when 0 then 'incompleted'
    end as amount,
case dzz.delerivered_status
    when 1 then 'delivered'
    when 0 then 'Pending'
 end as status    
FROM materials_order dzz
inner join materials_orderitem dop on  dop.order_id=dzz.id
left join materials_shippingaddress dxx on dxx.order_id=dzz.id
left join materials_courses dmf on dop.product_id=dmf.id
inner join auth_user ddd on ddd.id=dzz.customer_id
where dzz.customer_id = %s""",(userid,))
    details=cursor.fetchall()
    result=[]
    for detail in details:
        keys=('orderid','quantity','address','city','course_Name','price','course_Image','complete')
        result.append(dict(zip(keys,detail)))

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context={
        "detail":result,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'materials/orderhistory.html', context)

def delete_history(request,file_orderid):
    history=Order.objects.get(id=file_orderid)
    history.delete()
    return redirect('/materials/orderhistory/')

def mylearning(request):
    userid = request.user.id
    cursor = connection.cursor()
    cursor.execute("""SELECT  dmf.course_Name,dmf.course_Description,dmf.course_Image, dzz.id
    FROM materials_order dzz 
    inner join materials_orderitem dop on dop.order_id=dzz.id 
    left join materials_shippingaddress dxx on dxx.order_id=dzz.id
     left join materials_courses 
    dmf on dop.product_id=dmf.id inner join auth_user ddd on ddd.id=dzz.customer_id where 
    dzz.customer_id =%s and dzz.complete=1;
""", (userid,))
    details = cursor.fetchall()
    result = []
    for detail in details:
        keys = ('name', 'description', 'image','orderid')
        result.append(dict(zip(keys, detail)))

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {
        "detail": result,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request,'materials/mylearning.html',context)


def mymodule(request,file_orderid):
    course = Order.objects.get(id=file_orderid)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {
        'items': items,
               'order': order,
               'cartItems': cartItems,
               'detail':course,
               }
    return render(request,'materials/module.html',context)

def myquiz(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'items': items,
               'order': order,
               'cartItems': cartItems}
    return render(request,'materials/quiz.html',context)

def myweek(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'items': items,
               'order': order,
               'cartItems': cartItems}
    return render(request,'materials/week1.html',context)