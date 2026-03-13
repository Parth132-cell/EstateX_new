from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_videotour'),
    ]

    operations = [
        migrations.CreateModel(
            name='NegotiationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.BigIntegerField(db_index=True)),
                ('to_user', models.BigIntegerField(db_index=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('message', models.TextField(blank=True, default='')),
                ('offer_type', models.CharField(choices=[('offer', 'Offer'), ('counter', 'Counter')], db_index=True, default='offer', max_length=20)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='negotiations', to='listings.propertylisting')),
            ],
            options={
                'ordering': ['timestamp'],
                'indexes': [models.Index(fields=['listing', 'timestamp'], name='listings_neg_listing_0b20da_idx')],
            },
        ),
    ]
