# Generated by Django 3.0.5 on 2020-04-27 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_auto_20200426_2053'),
        ('Manage', '0004_auto_20200426_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_item',
            name='item_id',
        ),
        migrations.AddField(
            model_name='order_item',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='order_item',
            name='item_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order_item',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='account_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Account.Account'),
        ),
    ]
