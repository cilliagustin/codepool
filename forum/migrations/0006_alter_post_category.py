# Generated by Django 3.2.16 on 2023-01-13 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_alter_categories_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(max_length=60, on_delete=django.db.models.deletion.CASCADE, related_name='catego', to='forum.categories'),
        ),
    ]