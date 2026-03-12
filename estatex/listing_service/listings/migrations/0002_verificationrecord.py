from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_lat', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('geo_lng', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('face_match_score', models.DecimalField(decimal_places=3, max_digits=4)),
                ('ai_fraud_score', models.DecimalField(decimal_places=3, max_digits=4)),
                ('gps_metadata_present', models.BooleanField(default=False)),
                ('timestamp_valid', models.BooleanField(default=False)),
                ('result', models.CharField(choices=[('pending_admin', 'Pending Admin Approval'), ('failed', 'Failed')], max_length=20)),
                ('admin_approval_required', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_records', to='listings.propertylisting')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
