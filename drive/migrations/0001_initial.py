# Generated by Django 4.0.5 on 2022-06-26 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DriveFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('starred', models.BooleanField(default=False)),
                ('trashed', models.BooleanField(default=False)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('icon_url', models.CharField(blank=True, max_length=255, null=True)),
                ('created_time', models.DateTimeField(null=True)),
                ('modified_time', models.DateTimeField(null=True)),
                ('social', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='socialaccount.socialaccount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
