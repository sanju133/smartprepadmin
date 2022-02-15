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
            form.save()
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
    course=Courses.objects.all().order_by('-id')
    context={
        'course':course,
    }
    return render(request, 'lecturer/get_course.html', context)

#lectures Form
def lectures_form(request):
    if request.method=="POST":
        form=LecturesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Lecture added successfully')
            return redirect('/lecturer/get_lecture/')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add the Lecture')
            return render(request, 'lecturer/lecture_form.html', {'form_lecture': form})
    context = {
        'form_lecture': LecturesForm,
    }
    return render(request, 'lecturer/lecture_form.html', context)

# retrieving lecture form
def get_lecture(request):
    lecture=Lectures.objects.all().order_by('-id')
    context={
        'lecture':lecture
    }

    return render(request,'lecturer/get_lecture.html', context)
