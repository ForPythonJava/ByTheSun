# Generated by Django 4.2.2 on 2023-07-01 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.CharField(max_length=300)),
                ('date', models.DateField()),
                ('shopid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.shop')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
    ]
