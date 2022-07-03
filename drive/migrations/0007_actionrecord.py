# Generated by Django 4.0.5 on 2022-06-27 17:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0006_remove_drivefile_starred_remove_drivefile_trashed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='drive.drivefile')),
            ],
        ),
    ]