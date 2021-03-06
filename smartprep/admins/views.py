from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
from accounts.auth import admin_only
from django.db import connection
from accounts.models import *
from materials.models import *

from materials.forms import CategoriesForm, CoursesForm, LecturesForm
from materials.models import Categories, Courses, Lectures

@login_required
@admin_only
def admin_dashboard(request):
    category=Categories.objects.all()
    category_count=category.count()

    orders = Order.objects.all()
    orders_count = orders.count()

    contact = Contact.objects.all()
    contact_count = contact.count()

    users = User.objects.all()
    user_count = users.filter(is_staff=0).count()
    admin_count = users.filter(is_staff=1, is_superuser=0).count()
    lecture_count = users.filter(is_staff=1 ,is_superuser=0).count()

    context = {
        'order': orders_count,
        'category':category_count,
        'user': user_count,
        'admin': admin_count,
        'contact':contact_count,
        'lecture':lecture_count,
        'activate_dashboard': 'active'

    }
    return render(request, 'admins/admin_dashboard.html',context)

def form(request):
    return render(request, 'admins/form.html')

def show_course(request):
    return render(request, 'admins/show_course.html')

def show_contact(request):
    return render(request, 'admins/show_contact.html')


# retrieving category form
@login_required
@admin_only
def categories_form(request):
    if request.method == "POST":
        form = CategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category added successfully')
            return redirect("/admins/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add the category')
            return render(request, 'admins/category_form.html', {'form_category':form})
    context ={
        'form_category': CategoriesForm,

    }
    return render(request, 'admins/category_form.html', context)

#
# retrieving category
@login_required
@admin_only
def get_category(request):
    category=Categories.objects.all().order_by('-id')

    context={
        'category':category,
        'activate_category_admin':'active'
    }
    return render(request, 'admins/get_category.html', context)
# #deleting category
# @login_required
# @admin_only
# def delete_category(request, categories_id):
#     category=Categories.objects.get(id=categories_id)
#     category.delete()
#     messages.add_message(request, messages.SUCCESS, 'Category Deleted!')
#     return redirect('/admins/get_category/')


#deleting course
def delete_category(request, categories_id):
    category=Categories.objects.get(id=categories_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category Deleted!')
    return redirect('/admins/get_category/')



# update category
def category_update_form(request, categories_id):
    category = Categories.objects.get(id=categories_id)
    if request.method == "POST":
        if request.FILES.get('categories_Image'):
            os.remove(category.categories_Image.path)
        form = CategoriesForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated successfully')
            return redirect("/admins/get_category/")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update')
            return render(request, 'admins/category_update_form.html', {'form_category_update':category})
    context ={
        'form_category_update': CategoriesForm(instance=category),
        'activate_category':'active'
    }
    return render(request, 'admins/category_update_form.html', context)

# retrieving contact
def show_contact(request):
    contact=Contact.objects.filter(status='Mark as read').order_by('-created_date')

    context={
        'contact_admin':contact,
        'activate_contact':'active_admin'
    }
    return render(request, 'admins/show_contact.html', context)

#
#
def mark_as_read(request, contact_id):
    message=Contact.objects.get(id=contact_id)
    message.status="Seen"
    message.save()

    return redirect('/admins/show_contact')



# order history for admin
@login_required
@admin_only
def order(request):
    userid = request.user.id
    cursor = connection.cursor()
    cursor.execute("""SELECT dzz.id,ddd.username, dop.quantity,dxx.address,dxx.city,dmf.course_Name,dmf.price,dmf.course_Image,
    case dzz.complete
            when 1 then 'completed'
            when 0 then 'incompleted'
        end as amount,
    case dzz.delerivered_status
        when 1 then 'delivered'
        when 0 then 'Pending'
     end as status    
    FROM materials_order dzz
    left join materials_orderitem dop on  dop.order_id=dzz.id
    left join materials_shippingaddress dxx on dxx.order_id=dzz.id
    left join materials_courses dmf on dop.product_id=dmf.id
    left join auth_user ddd on ddd.id=dzz.customer_id """)
    details = cursor.fetchall()
    result = []
    for detail in details:
        keys = ('orderid', 'username','quantity', 'address', 'city', 'course_Name', 'price', 'course_Image', 'complete')
        result.append(dict(zip(keys, detail)))


    context = {
        "detail": result,
        'activate_payment_admin': 'active'

    }

    return render(request, 'admins/order_details.html', context)


@login_required
@admin_only
def get_users(request):
    users = User.objects.filter(is_staff=0).order_by('-id')

    context = {
        'users':users,
        'activate_user': 'active',


    }
    return render(request, 'admins/users.html', context)

@login_required
@admin_only
def get_admins(request):
    admins = User.objects.filter(is_staff=1, is_superuser=1).order_by('-id')
    context = {
        'admins':admins,
        'activate_admin': 'active',
    }
    return render(request, 'admins/admins.html', context)


@login_required
@admin_only
def get_lecture(request):
    lecture = User.objects.filter(is_staff=1 ,is_superuser=0).order_by('-id')
    context = {
        'lecture':lecture,
        'activate_lecture': 'active',
    }
    return render(request, 'admins/lecture.html', context)

@login_required
@admin_only
def promote_user(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_staff=True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'User promoted to admin')
    return redirect('/admins/admins')

@login_required
@admin_only
def demote_user(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_staff=False
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Admin demoted to user')
    return redirect('/admins/users')

@login_required
@admin_only
def delete_user(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('/admins/users')

@login_required
@admin_only
def delete_admin(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('/admins/admins')

@login_required
@admin_only
def add_lecture(request):
    if request.method =="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('username')
            user=User.objects.create_user(username=username,
                                   email=email)
            user.is_staff=True
            user.is_superuser=False


            user.save()


            return redirect('/admins/add_lecture/')
        else:
            messages.add_message(request, messages.ERROR,'Sorry! ,Something went wrong')
            return render(request, 'admins/add_lecture.html',{'form_admin':form})
    context = {
        'form_admin': CreateUserForm,
        'activate_admin': 'active',

    }
    return render(request,'admins/add_lecture.html',context)


@login_required
@admin_only
# get perticular course
def get_particular_course(request, categories_id):
    categories=Categories.objects.get(id=categories_id)
    context={
        'categories':categories
    }
    return render(request, 'admins/get_particular_course.html', context)

@login_required
def password_change(request):
    if request.method=='POST':
        # new_password1 = request.POST.get('new_password1')
        # new_password2 = request.POST.get('new_password2')
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.add_message(request,messages.SUCCESS,"Password changed successfully!")
            return redirect('/password_change/')
        else:
            # if User.objects.filter(new_password1=new_password1).exists():
            #     messages.add_message(request, messages.ERROR,'username already exists')
            #     return redirect('/RegisterForm/')
            messages.add_message(request,messages.ERROR, "Something went wrong!")
            return render(request,'accounts/password_change.html', {'password_change_form':form})
    context={
        'password_change_form':PasswordChangeForm(request.user),
        'activate_password': 'active',
    }
    return render(request,'accounts/password_change.html',context)