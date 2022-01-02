# Generated by Django 3.2.10 on 2021-12-28 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbacks',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.profiles'),
        ),
        migrations.AlterUniqueTogether(
            name='feedbacks',
            unique_together={('owner', 'offer')},
        ),
    ]
