# Generated by Django 4.2.11 on 2024-05-23 19:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('model', '0006_methodologies_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterias',
            name='access',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
