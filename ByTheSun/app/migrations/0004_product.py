# Generated by Django 4.2.2 on 2023-06-28 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='image')),
                ('price', models.IntegerField()),
            ],
        ),
    ]
