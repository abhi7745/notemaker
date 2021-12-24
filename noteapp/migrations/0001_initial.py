# Generated by Django 3.1.1 on 2021-08-04 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='note',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
