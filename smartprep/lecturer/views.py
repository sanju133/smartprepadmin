import os

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from materials.forms import  CoursesForm, LecturesForm
from materials.models import Courses, Lectures, Categories


def lecturer_dashboard(request):
    return render(request, 'lecturer/lecturer_dashboard.html')

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
    }
    return render(request, 'lecturer/course_form.html', context)

# retrieving course
def get_course(request):
    User=request.user
    course=Courses.objects.filter(user=User).order_by('-id')
    context={
        'course':course,

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
    }
    return render(request, 'lecturer/lecture_form.html', context)
def get_lecture(request):
    User=request.user
    lecture=Lectures.objects.filter(user=User).order_by('-id')
    context={
        'lecture':lecture
    }



    return render(request,'lecturer/get_lecture.html', context)

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
        'course':courseDetail
    }
    return render(request, 'lecturer/get_particular_lecture.html', context)

#deleting lecture
def delete_lecture(request, lectures_id):
    lecture=Lectures.objects.get(id=lectures_id)
    lecture.delete()
    messages.add_message(request, messages.SUCCESS, 'Lecture Deleted!')
    return redirect('/lecturer/get_course/')



