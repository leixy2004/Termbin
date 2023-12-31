# Generated by Django 4.2.5 on 2023-10-05 15:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tbin', '0003_paste_short_id_alter_paste_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50)),
                ('password_sha256', models.CharField(max_length=70)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='paste',
            name='paste_digest',
            field=models.CharField(max_length=70),
        ),
        migrations.AddField(
            model_name='paste',
            name='author',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='tbin.user'),
            preserve_default=False,
        ),
    ]
