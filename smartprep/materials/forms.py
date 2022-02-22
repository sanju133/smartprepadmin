from django import forms
from  django.forms import ModelForm
from .models import Categories, Courses, Lectures


class CategoriesForm(ModelForm):
    class Meta:
        model=Categories
        fields='__all__'

class CoursesForm(ModelForm):
    class Meta:
        model=Courses
        fields=['course_Name', 'category_Courses', 'course_Description',
                'course_Image', 'price','digital']

 # course_Name=models.CharField(max_length=1000)
 #    category=models.ForeignKey(Categories, on_delete=models.CASCADE)
 #    course_Description = models.TextField(validators=[MinLengthValidator(9), MaxLengthValidator(3000)],
 #
 #                                            null=True, max_length=3000)
 #    course_Image = models.FileField(upload_to='static/uploaded_Files')
 #    price=models.FloatField(default=20)
 #    digital=models.BooleanField(default=False,null=True,blank=False)
 #    def __str__(self):
 #        return self.course_Name
class LecturesForm(ModelForm):
    class Meta:
        model=Lectures
        fields = ['lecture_Name', 'course','lecture_content' ]


# class CommentForm(ModelForm):
#     class Meta:
#         model=Comments
#         fields=['content']
#
