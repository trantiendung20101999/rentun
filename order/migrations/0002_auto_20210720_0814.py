# Generated by Django 3.2.5 on 2021-07-20 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210720_0507'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='order.cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('is_bought', models.BooleanField(default=False)),
                ('cart', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]