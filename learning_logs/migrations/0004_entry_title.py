# Generated by Django 4.1.3 on 2022-12-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
