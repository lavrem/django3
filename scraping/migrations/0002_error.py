# Generated by Django 3.2.8 on 2021-11-24 11:13

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Ошибка',
                'verbose_name_plural': 'Ошибки',
            },
        ),
    ]