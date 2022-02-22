# Generated by Django 3.2.6 on 2022-02-22 17:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_Name', models.CharField(max_length=1000, null=True, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(1000)])),
                ('category_Description', models.TextField(max_length=1000, null=True, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(3000)])),
                ('category_Image', models.FileField(upload_to='static/uploaded_Files')),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_Name', models.CharField(max_length=1000)),
                ('course_Description', models.TextField(max_length=3000, null=True, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(3000)])),
                ('course_Image', models.FileField(upload_to='static/uploaded_Files')),
                ('price', models.FloatField(default=20)),
                ('digital', models.BooleanField(default=False, null=True)),
                ('category_Courses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.categories')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('delerivered_status', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('data_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Lectures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_Name', models.CharField(max_length=100)),
                ('lecture_content', models.TextField(max_length=1000, null=True, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(3000)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.courses')),
            ],
        ),
    ]
