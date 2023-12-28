# Generated by Django 5.0 on 2023-12-25 18:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0002_rename_acknowledgement_date_purchaseorder_acknowledged_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='on_time_delevery_rate',
            new_name='on_time_delivery_rate',
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchaser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='vms.purchaser'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='quality_rating',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Canceled'), ('D', 'Delivered')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='vms.vendor'),
        ),
    ]