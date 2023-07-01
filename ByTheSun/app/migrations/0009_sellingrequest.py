# Generated by Django 4.2.2 on 2023-07-01 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_booking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.IntegerField()),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('date', models.DateField(auto_now=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
    ]
