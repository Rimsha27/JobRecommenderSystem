# Generated by Django 2.0.4 on 2018-05-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_workexperiencemodel_feedbackforjob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='enddateedu',
        ),
        migrations.RemoveField(
            model_name='education',
            name='startdateedu',
        ),
        migrations.RemoveField(
            model_name='workexperiencemodel',
            name='endDate',
        ),
        migrations.RemoveField(
            model_name='workexperiencemodel',
            name='startDate',
        ),
        migrations.AddField(
            model_name='education',
            name='yearofedu',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workexperiencemodel',
            name='year',
            field=models.CharField(max_length=100, null=True),
        ),
    ]