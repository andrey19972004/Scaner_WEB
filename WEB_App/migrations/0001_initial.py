# Generated by Django 3.0.3 on 2020-04-01 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='photos', verbose_name='Ссылка на s3 хранилище')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('target_good', models.TextField(null=True, verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='UserPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='profile_icon', null=True, upload_to='profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recovery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_ip', models.CharField(default=None, max_length=15)),
                ('code', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RatePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, 'Ужасно'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')], default=1)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB_App.Picture', verbose_name='Фото')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsOnModeration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255, verbose_name='Наименование')),
                ('image', models.ImageField(null=True, upload_to='photos', verbose_name='Ссылка на s3 хранилище')),
                ('barcode', models.TextField(db_index=True, default=None, null=True, verbose_name='Штрих-код')),
                ('status', models.CharField(choices=[(1, 'Принято на модерацию'), (2, 'Обработано'), (3, 'Отклонено')], default=1, max_length=25, verbose_name='Статус')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Содержимое комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('good', models.TextField(verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='ChildrenComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Содержимое комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEB_App.Comment', verbose_name='Комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
