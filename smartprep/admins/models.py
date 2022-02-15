# from django.core.validators import MinLengthValidator, MaxLengthValidator
# from django.db import models
#
# # Create your models here.
# # categories table
# class Categories(models.Model):
#     category_Name=models.CharField(validators=[MinLengthValidator(9), MaxLengthValidator(1000)],
#                                   null=True, max_length=1000)
#
#     category_Description=models.TextField(validators=[MinLengthValidator(9), MaxLengthValidator(3000)],
#                                   null=True, max_length=3000)
#     category_Image=models.FileField(upload_to='static/uploaded_Files')
#     def __str__(self):
#         return self.category_Name
#
#
# # courses table
# class Courses(models.Model):
#     course_Name=models.CharField(max_length=1000)
#     category=models.ForeignKey(Categories, on_delete=models.CASCADE)
#     course_Description = models.TextField(validators=[MinLengthValidator(9), MaxLengthValidator(3000)],
#
#                                             null=True, max_length=3000)
#     course_Image = models.FileField(upload_to='static/uploaded_Files')
#     def __str__(self):
#         return self.course_Name
#
#
# # lecturers table
# class Lectures(models.Model):
#     lecture_Name=models.CharField(max_length=3000)
#     course = models.ForeignKey(Courses, on_delete=models.CASCADE)
#     lecture_content= models.TextField(validators=[MinLengthValidator(9), MaxLengthValidator(3000)],
#                                             null=True, max_length=3000)
#     def __str__(self):
#         return self.lecture_Name
