# Generated by Django 5.0.3 on 2024-11-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0003_alter_sora_userinfo_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sora_userinfo",
            name="password",
            field=models.BinaryField(verbose_name="密码"),
        ),
    ]
