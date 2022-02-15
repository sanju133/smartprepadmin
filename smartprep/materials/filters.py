import django_filters
from .models import Courses, Categories
from django_filters import CharFilter

# for filtering books
class CourseFilter(django_filters.FilterSet):
    course_name_contain=CharFilter(field_name='course_Name', lookup_expr='icontains')
    class Meta:
        model=Courses
        fields=[]




class CatFilter(django_filters.FilterSet):
    cat_name_contain=CharFilter(field_name='category_Name', lookup_expr='icontains')
    class Meta:
        model=Categories
        fields=[]