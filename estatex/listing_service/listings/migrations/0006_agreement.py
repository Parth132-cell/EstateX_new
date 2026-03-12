from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_id', models.BigIntegerField(db_index=True)),
                ('seller_id', models.BigIntegerField(db_index=True)),
                ('template_name', models.CharField(max_length=120)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('generated', 'Generated'), ('sent', 'Sent for eSign'), ('signed', 'Signed')], db_index=True, default='generated', max_length=20)),
                ('esign_provider', models.CharField(blank=True, default='', max_length=80)),
                ('esign_request_id', models.CharField(blank=True, db_index=True, default='', max_length=120)),
                ('signed_pdf_url', models.URLField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='listings.propertylisting')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
