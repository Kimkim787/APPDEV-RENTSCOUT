# Generated by Django 4.2.4 on 2024-12-26 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0024_alter_message_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='roomid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_room', to='RentScout.room'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentid', models.AutoField(primary_key=True, serialize=False)),
                ('referralid', models.CharField(default='', max_length=60)),
                ('payment_img', models.FileField(default='upload/payments/gcash_receipt.jpg', upload_to='upload/payments')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Pending', max_length=10)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('boarder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_sender', to='RentScout.scoutuser')),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_payed', to='RentScout.room')),
            ],
            options={
                'ordering': ['date_sent'],
            },
        ),
    ]
