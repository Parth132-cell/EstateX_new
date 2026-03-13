from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_verificationrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('host_id', models.BigIntegerField(db_index=True)),
                ('scheduled_at', models.DateTimeField(db_index=True)),
                ('recording_url', models.URLField(blank=True, default='')),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('live', 'Live'), ('ended', 'Ended')], db_index=True, default='scheduled', max_length=20)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_tours', to='listings.propertylisting')),
            ],
            options={
                'ordering': ['-scheduled_at'],
            },
        ),
    ]
