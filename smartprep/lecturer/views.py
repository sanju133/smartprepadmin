import os

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from materials.forms import  CoursesForm, LecturesForm
from materials.models import Courses, Lectures, Categories
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from accounts.models import *
from django.contrib.auth.decorators import login_required


def lecturer_dashboard(request):
    course= Courses.objects.all()
    course_count = course.count()

    lecture = Lectures.objects.all()
    lecture_count = lecture.count()


    users = User.objects.all()
    user_count = users.filter(is_staff=0).count()
    context={
        'activate_dashboard': 'active',
        'course': course_count,
        'lecture': lecture_count,
        'user': user_count,


    }
    return render(request, 'lecturer/lecturer_dashboard.html',context)

# Courses Form
def courses_form(request):
    if request.method=='POST':
        form=CoursesForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save()
            instance.user=request.user
            instance.save()
            messages.add_message(request,messages.SUCCESS, 'Course added successfully!')
            return redirect('/lecturer/get_course/')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add the Course')
            return render(request,'lecturer/course_form.html', {'form_course':form})
    context ={
        'form_course': CoursesForm,
        'activate_course': 'active',
    }
    return render(request, 'lecturer/course_form.html', context)

# retrieving course
def get_course(request):
    User=request.user
    course=Courses.objects.filter(user=User).order_by('-id')
    context={
        'course':course,
        'activate_course': 'active',

    }
    return render(request, 'lecturer/get_course.html', context)

#deleting course
def delete_course(request, courses_id):
    course=Courses.objects.get(id=courses_id)
    course.delete()
    messages.add_message(request, messages.SUCCESS, 'Course Deleted!')
    return redirect('/lecturer/get_course/')

# update course
def course_update_form(request, courses_id):
    course= Courses.objects.get(id=courses_id)
    if request.method == "POST":
        if request.FILES.get('course_Image'):
            os.remove(course.course_Image.path)
        form = CoursesForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Course updated successfully')
            return redirect("/lecturer/get_course/")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update')
            return render(request, 'lecturer/course_update_form.html', {'form_course_update':course})
    context ={
        'form_course_update': CoursesForm(instance=course),
        'activate_course':'active'
    }
    return render(request, 'lecturer/course_update_form.html', context)

#lectures Form
def lectures_form(request):
    if request.method=="POST":
        form=LecturesForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.add_message(request,messages.SUCCESS,'Lecture added successfully')
            return redirect('/lecturer/get_lecture/')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add the Lecture')
            return render(request, 'lecturer/lecture_form.html', {'form_lecture': form})
    context = {
        'form_lecture': LecturesForm,
        'activate_addlecture': 'active',
    }
    return render(request, 'lecturer/lecture_form.html', context)

#getting lecture that you added only
def get_lecture(request):
    User=request.user
    lecture=Lectures.objects.filter(user=User).order_by('-id')
    context={
        'lecture':lecture,
        'activate_lecture': 'active',
    }



    return render(request,'lecturer/get_lecture.html', context)

#lecture update form
def lecture_update_form(request, lectures_id):
    lecture= Lectures.objects.get(id=lectures_id)
    if request.method == "POST":
        # if request.FILES.get('course_Image'):
        #     os.remove(lecture.course_Image.path)
        form = LecturesForm(request.POST, request.FILES, instance=lecture)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Lecture updated successfully')
            return redirect("/lecturer/get_lecture/")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update')
            return render(request, 'lecturer/lecture_update_form.html', {'form_lecture_update':lecture})
    context ={
        'form_lecture_update': LecturesForm(instance=lecture),
        'activate_lecture':'active'
    }
    return render(request, 'lecturer/lecture_update_form.html', context)

# get perticular lecture
def get_particular_lecture(request, courses_id):
    courseDetail=Courses.objects.get(id=courses_id)
    context={
        'course':courseDetail,
        'activate_lecture': 'active',
    }
    return render(request, 'lecturer/get_particular_lecture.html', context)

#deleting lecture
def delete_lecture(request, lectures_id):
    lecture=Lectures.objects.get(id=lectures_id)
    lecture.delete()
    messages.add_message(request, messages.SUCCESS, 'Lecture Deleted!')
    context={
        'activate_lecture': 'active',
    }
    return redirect('/lecturer/get_course/',context)



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
            return redirect('/lecturer/password_change/')
        else:
            # if User.objects.filter(new_password1=new_password1).exists():
            #     messages.add_message(request, messages.ERROR,'username already exists')
            #     return redirect('/RegisterForm/')
            messages.add_message(request,messages.ERROR, "Something went wrong!")
            return render(request,'lecturer/password_change.html', {'password_change_form':form})
    context={
        'password_change_form':PasswordChangeForm(request.user),
        'activate_password': 'active',
    }
    return render(request,'lecturer/password_change.html',context)