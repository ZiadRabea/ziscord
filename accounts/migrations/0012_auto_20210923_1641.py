# Generated by Django 3.1.4 on 2021-09-23 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_profile_chatters'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='message',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replied_msg', to='accounts.message'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]