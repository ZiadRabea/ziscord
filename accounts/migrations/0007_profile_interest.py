# Generated by Django 3.1.4 on 2021-09-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_searching_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interest',
            field=models.CharField(choices=[('Technology', 'Technology'), ('handmade', 'handmade'), ('software development', 'software development'), ('Cars', 'Cars'), ('Jobs', 'Jobs'), ('Freelancing', 'Freelancing'), ('Animals', 'Animals')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]