# Generated by Django 3.1 on 2020-08-12 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('to_do', '0006_delete_todoitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, help_text='Add more details here. You can use markdown to format it!')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('priority', models.IntegerField(default=1)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_items', to='to_do.todolist')),
            ],
        ),
    ]
