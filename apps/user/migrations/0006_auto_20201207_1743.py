# Generated by Django 3.1.1 on 2020-12-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_user_avatar_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
