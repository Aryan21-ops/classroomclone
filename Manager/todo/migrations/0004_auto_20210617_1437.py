# Generated by Django 2.2.5 on 2021-06-17 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20210609_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todotasks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_todo', to=settings.AUTH_USER_MODEL),
        ),
    ]
