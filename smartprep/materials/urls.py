from django.urls import path

from materials import views
urlpatterns = [

   # path('home', views.content2),
    path('home/', views.home),
    path('courses/', views.course),
    path('get_course_category/<int:categories_id>', views.get_course_category),
    path('cart/',views.cart),
    path('checkout/',views.checkout),
    path('update_item/',views.updateItem),

    path('process_order/', views.processOrder),
    path('details/<int:i_id>/', views.details),

    path('orderhistory/',views.orderhistory),
    path('delete_history/<int:file_orderid>',views.delete_history),

    path('mylearning/',views.mylearning),
    path('module/', views.mymodule),
    path('quiz/', views.myquiz),
    path('week1/', views.myweek),
    # path('content/', views.content2)

]