# Generated by Django 3.1.7 on 2021-03-09 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210309_1108'),
        ('products', '0004_auto_20210309_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprofile',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile'),
        ),
    ]
