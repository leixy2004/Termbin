# Generated by Django 4.2.5 on 2023-10-07 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbin', '0008_alter_paste_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paste',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
