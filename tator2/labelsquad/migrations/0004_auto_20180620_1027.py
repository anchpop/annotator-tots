# Generated by Django 2.0.6 on 2018-06-20 14:27

from django.db import migrations, models
import labelsquad.models


class Migration(migrations.Migration):

    dependencies = [
        ('labelsquad', '0003_auto_20180620_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagecollection',
            name='classes',
        ),
        migrations.AddField(
            model_name='project',
            name='classes',
            field=models.ManyToManyField(to='labelsquad.ObjectClass'),
        ),
        migrations.AlterField(
            model_name='imagecollection',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='imagecollection',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='objectclass',
            name='class_type',
            field=models.CharField(choices=[('Polygon', 'Polygon'), ('Whole image', 'Whole image')], default=labelsquad.models.ClassTypeChoices('Polygon'), max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='collections',
            field=models.ManyToManyField(null=True, to='labelsquad.ImageCollection'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
