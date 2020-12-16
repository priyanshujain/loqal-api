# Generated by Django 3.1.1 on 2020-12-16 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0008_remove_merchantprofile_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchantprofile',
            old_name='logo',
            new_name='hero_image',
        ),
        migrations.RenameField(
            model_name='merchantprofile',
            old_name='istagram_page',
            new_name='instagram_page',
        ),
        migrations.AddField(
            model_name='merchantprofile',
            name='category',
            field=models.CharField(default='shopping', max_length=64),
        ),
        migrations.AddField(
            model_name='merchantprofile',
            name='sub_category',
            field=models.CharField(default='antiques_jewelry', max_length=64),
        ),
    ]
