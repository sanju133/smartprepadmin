from django.urls import path

from admins import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard),
    path('category_form/', views.categories_form),
    path('get_category/', views.get_category),

    path('show_course/', views.show_course),
    path('show_contact/', views.show_contact),
    path('form/', views.form),
    path('delete_category/<int:categories_id>', views.delete_category),
path('orderhistory/',views.order),

    path('users/', views.get_users),
    path('admins/', views.get_admins),

    path('delete_user/<int:user_id>', views.delete_user),
    path('delete_admin/<int:user_id>', views.delete_admin),

    path('promote_user/<int:user_id>', views.promote_user),
    path('demote_user/<int:user_id>', views.demote_user),

]