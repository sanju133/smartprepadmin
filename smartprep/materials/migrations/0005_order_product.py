# Generated by Django 3.2.6 on 2022-03-06 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_alter_courses_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.courses'),
        ),
    ]