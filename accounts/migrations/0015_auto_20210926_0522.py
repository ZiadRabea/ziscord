# Generated by Django 3.1.4 on 2021-09-26 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_group_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='Chatting files'),
        ),
        migrations.AddField(
            model_name='group_message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Chatting images'),
        ),
    ]