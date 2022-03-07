from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from accounts.forms import CreateUserForm

# Create your models here.
# categories table
class Categories(models.Model):
    category_Name=models.CharField(validators=[MinLengthValidator(9), MaxLengthValidator(1000)],
                                  null=True, max_length=1000)

    category_Description=models.TextField(validators=[MinLengthValidator(9), MaxLengthValidator(3000)],
                                  null=True, max_length=1000)
    category_Image=models.FileField(upload_to='static/uploaded_Files')
    def __str__(self):
        return self.category_Name


# courses table
class Courses(models.Model):
    file = models.FileField(blank=True, upload_to='static/pdf_uploads', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_Name=models.CharField(max_length=1000)
    category_Courses=models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    course_Description = models.TextField(validators=[MinLengthValidator(9), MaxLengthValidator(3000)],

                                            null=True, max_length=3000)
    course_Image = models.FileField(upload_to='static/uploaded_Files')
    price=models.FloatField(default=20)
    digital=models.BooleanField(default=False,null=True,blank=False)
    def __str__(self):
        return self.course_Name



class Order (models.Model):
    customer=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100, null=True)
    delerivered_status=models.BooleanField(default=False)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product=models.ForeignKey(Courses, on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    data_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address=models.CharField(max_length=200, null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200, null=True)
    date_added =models.DateTimeField(auto_now_add=True)


# lecturers table
class Lectures(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    lecture_Name=models.CharField(max_length=100, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    lecture_content= RichTextField(validators=[MinLengthValidator(9), MaxLengthValidator(15000)],
                                            null=True, max_length=15000)
    def __str__(self):
        return self.lecture_Name

class Comments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    content=models.TextField(max_length=250)
    created_Date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.content)