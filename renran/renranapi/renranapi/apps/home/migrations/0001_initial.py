# Generated by Django 2.2 on 2020-03-06 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.IntegerField(verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('image', models.ImageField(blank=True, null=True, upload_to='banner', verbose_name='轮播图')),
                ('name', models.CharField(max_length=150, verbose_name='轮播图标题')),
                ('note', models.CharField(max_length=500, verbose_name='备注信息')),
                ('link', models.CharField(max_length=150, verbose_name='轮播图广告地址')),
                ('start_time', models.DateTimeField(verbose_name='开始展示时间')),
                ('end_time', models.DateTimeField(verbose_name='结束展示时间')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'db_table': 'rr_banner',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='标题')),
                ('orders', models.IntegerField(verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('is_http', models.BooleanField(default=True, help_text='如果是站内地址,则默认勾选', verbose_name='是否站内的链接')),
                ('link', models.CharField(help_text='如果是站外链接,必须加上协议, 格式如: http://www.renran.cn', max_length=500, verbose_name='导航地址')),
                ('option', models.SmallIntegerField(choices=[(1, '头部导航'), (2, '脚部导航')], default=1, verbose_name='导航位置')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='son', to='home.Nav', verbose_name='父亲导航')),
            ],
            options={
                'verbose_name': '导航菜单',
                'verbose_name_plural': '导航菜单',
                'db_table': 'rr_nav',
            },
        ),
    ]
