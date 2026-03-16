from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_agreement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raised_by_user_id', models.BigIntegerField(db_index=True)),
                ('reason', models.TextField()),
                ('resolution_notes', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('open', 'Open'), ('resolved', 'Resolved')], db_index=True, default='open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputes', to='listings.propertylisting')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
