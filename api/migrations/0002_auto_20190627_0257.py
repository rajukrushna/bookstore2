# Generated by Django 2.2.2 on 2019-06-26 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pdf',
            field=models.FileField(blank=True, upload_to='files/'),
        ),
    ]
