# Generated by Django 5.1.4 on 2025-02-18 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DateBaseApp', '0005_alter_user_email_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogForDeleteUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=128)),
                ('delete_user', models.CharField(max_length=20)),
            ],
        ),
    ]
