# Generated by Django 3.2.6 on 2022-03-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_courses_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static/pdf_uploads'),
        ),
    ]
