# Generated by Django 2.2 on 2020-06-07 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_delete_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='last_reg_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='event',
            name='page_visits',
            field=models.IntegerField(default=0),
        ),
    ]
