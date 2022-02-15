from django.shortcuts import redirect

# to check if the user is logged in or not
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/materials/home/')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

# give access to admin pages if request comes from admin
# if request is from normal user, redirects to learner dashboard
# if request is from lecturer, redirects to lecturer dashboard
def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff==1 & request.user.is_superuser==1:
            return view_function(request, *args, **kwargs)
        elif request.user.is_staff==0 & request.user.is_superuser==0:
            return redirect('/materials/home/')
        else:
            return redirect('/lecturer/lecturerDashboard/')
    return wrapper_function

# give access to normal user pages if request comes from learner
# if request is from admin user, redirects to admin dashboard
# if request is from lecturer, redirects to lecturer dashboard
def learner_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff==0 & request.user.is_superuser==0:
            return view_function(request, *args, **kwargs)
        elif request.user.is_staff == 1 & request.user.is_superuser == 1:
            return redirect('/admins/dashboard')
        else:
            return redirect('/lecturer/lecturerDashboard/')
    return wrapper_function

# give access to lecturer pages if request comes from lecturer
# if request is from admin user, redirects to admin dashboard
# if request is from normal user, redirects to learner
def lecturer_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff==1 and request.user.is_superuser==0:
            return view_function(request, *args, **kwargs)
        elif request.user.is_staff == 1 & request.user.is_superuser == 1:
            return redirect('/admins/dashboard/')
        else:
            return redirect('/materials/home/')
    return wrapper_function