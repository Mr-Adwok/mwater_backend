# Generated by Django 5.1.6 on 2025-02-15 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_account_id', models.CharField(max_length=50)),
                ('meter_photo', models.ImageField(upload_to='meter_photos/')),
                ('payment_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='billpayment',
            name='user',
        ),
        migrations.DeleteModel(
            name='OTP',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_staff',
            new_name='is_verified',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='bill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.user'),
        ),
        migrations.DeleteModel(
            name='BillPayment',
        ),
    ]
