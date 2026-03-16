from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PropertyListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker_id', models.BigIntegerField(db_index=True)),
                ('title', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(db_index=True, max_length=120)),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=14)),
                ('bhk', models.PositiveSmallIntegerField(db_index=True)),
                ('description', models.TextField()),
                ('amenities', models.JSONField(default=list)),
                ('verification_status', models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')], db_index=True, default='pending', max_length=20)),
                ('media_urls', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['city', 'price'], name='listings_pr_city_3f966a_idx'), models.Index(fields=['city', 'bhk'], name='listings_pr_city_06d86b_idx'), models.Index(fields=['price', 'bhk'], name='listings_pr_price_1144be_idx')],
            },
        ),
    ]
