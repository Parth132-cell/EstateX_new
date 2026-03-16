from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_negotiationhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_id', models.BigIntegerField(db_index=True)),
                ('seller_id', models.BigIntegerField(db_index=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('status', models.CharField(choices=[('order_created', 'Order Created'), ('funds_held', 'Funds Held'), ('released', 'Released'), ('failed', 'Failed')], db_index=True, default='order_created', max_length=20)),
                ('provider_reference', models.CharField(db_index=True, max_length=120, unique=True)),
                ('provider_order_id', models.CharField(blank=True, default='', max_length=120)),
                ('provider_payment_id', models.CharField(blank=True, default='', max_length=120)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='listings.propertylisting')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
