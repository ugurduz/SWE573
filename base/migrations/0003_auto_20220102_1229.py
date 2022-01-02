# Generated by Django 3.2.10 on 2022-01-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20211228_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendants',
            name='offerstatus',
            field=models.CharField(choices=[('done', 'Done'), ('canceled', 'Cancel'), ('inprogress', 'In Progress')], default=2, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedbacks',
            name='value',
            field=models.CharField(choices=[('up', 'Enjoyed'), ('down', 'Not Enjoyed')], max_length=50),
        ),
        migrations.AlterField(
            model_name='offers',
            name='type',
            field=models.CharField(choices=[('event', 'Offer'), ('gathering', 'Gathering')], max_length=50),
        ),
    ]
