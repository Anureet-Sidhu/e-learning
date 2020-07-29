# Generated by Django 3.0.6 on 2020-07-17 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20200717_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='myapp.Student'),
        ),
    ]