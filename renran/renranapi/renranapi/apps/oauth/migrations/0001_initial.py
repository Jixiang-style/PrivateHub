# Generated by Django 2.2 on 2020-03-18 04:04

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
            name='OAuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='标题')),
                ('orders', models.IntegerField(verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('openid', models.CharField(db_index=True, max_length=64, verbose_name='openid')),
                ('access_token', models.CharField(help_text='有效期:3个月', max_length=500, verbose_name='临时访问票据')),
                ('refresh_token', models.CharField(help_text='当access_token以后,可以使用refresh_token来重新获取新的access_token', max_length=500, verbose_name='刷新访问票据的token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': 'QQ登录用户数据',
                'verbose_name_plural': 'QQ登录用户数据',
                'db_table': 'rr_oauth_qq',
            },
        ),
    ]
