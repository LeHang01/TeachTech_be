# Generated by Django 5.1.3 on 2024-12-10 08:44

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_user_is_teacher_user_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('meeting_type', models.CharField(default='Online Class', max_length=100)),
                ('date', models.DateTimeField()),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('Chưa bắt đầu', 'Chưa bắt đầu'), ('Đang diễn ra', 'Đang diễn ra'), ('Đã kết thúc', 'Đã kết thúc')], max_length=50)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('attachments', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Chưa tham gia', 'Chưa tham gia'), ('Đã tham gia', 'Đã tham gia'), ('Vắng', 'Vắng')], default='Chưa tham gia', max_length=20)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('absence_reason_type', models.CharField(blank=True, choices=[('Chính đáng', 'Chính đáng'), ('Không chính đáng', 'Không chính đáng')], max_length=20, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='app.meeting')),
            ],
        ),
    ]