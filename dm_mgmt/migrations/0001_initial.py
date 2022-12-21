# Generated by Django 4.1.3 on 2022-12-21 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('client_first_name', models.CharField(max_length=80, verbose_name='Prénom')),
                ('client_last_name', models.CharField(max_length=80, verbose_name='Nom')),
                ('client_birthdate', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('client_address', models.CharField(blank=True, max_length=80, null=True, verbose_name='Adresse')),
                ('client_additional_address', models.CharField(blank=True, max_length=80, null=True, verbose_name="Complément d'adresse")),
                ('client_zip_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='NPA')),
                ('client_city', models.CharField(blank=True, max_length=80, null=True, verbose_name='Localité')),
                ('client_phone_number_1', models.CharField(max_length=30, verbose_name='Téléphone 1')),
                ('client_phone_number_2', models.CharField(blank=True, max_length=30, null=True, verbose_name='Téléphone 2')),
                ('client_email_address', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('client_comment', models.TextField(blank=True, null=True, verbose_name='Commentaire')),
                ('client_is_displayed', models.BooleanField(default=True, verbose_name='Client à prendre en compte')),
            ],
            options={
                'ordering': ['client_last_name', 'client_first_name'],
            },
        ),
        migrations.CreateModel(
            name='Massage',
            fields=[
                ('massage_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('massage_name', models.CharField(max_length=80, verbose_name='Nom du massage')),
                ('massage_duration', models.PositiveSmallIntegerField(verbose_name='Durée (en minutes)')),
                ('massage_price', models.FloatField(verbose_name='Prix')),
                ('massage_is_available', models.BooleanField(default=False, verbose_name='Massage actuellement proposé')),
                ('massage_is_voucher', models.BooleanField(default=False, verbose_name='Bon / Abo')),
                ('massage_order', models.PositiveSmallIntegerField(default=0, verbose_name='Position')),
            ],
            options={
                'ordering': ['massage_order'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('service_date', models.DateField(verbose_name='Date du massage')),
                ('service_duration', models.PositiveSmallIntegerField(default=0, verbose_name='Durée du massage (en minutes)')),
                ('service_comment', models.TextField(blank=True, null=True, verbose_name='Remarque')),
                ('service_cashed_price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Montant encaissé (CHF)')),
                ('service_is_voucher', models.BooleanField(blank=True, default=False, verbose_name='Bon / abonnement')),
                ('service_client_id', models.ForeignKey(limit_choices_to={'client_is_displayed': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dm_mgmt.client', verbose_name='Client')),
                ('service_massage_id', models.ForeignKey(limit_choices_to={'massage_is_available': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dm_mgmt.massage', verbose_name='Massage')),
            ],
            options={
                'ordering': ['-service_date'],
            },
        ),
        migrations.CreateModel(
            name='ConsoService',
            fields=[
                ('client_id', models.IntegerField()),
                ('client_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('massage_name', models.CharField(max_length=255)),
                ('service_date', models.DateField()),
                ('service_cashed_price', models.FloatField()),
                ('service_is_voucher', models.BooleanField()),
            ],
            options={
                'db_table': 'dm_mgmt_conso_service',
                'ordering': ['-service_date'],
                'managed': False,
            },
        ),
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW public.dm_mgmt_conso_service
             AS
             SELECT dm_mgmt_client.client_id,
                concat(dm_mgmt_client.client_last_name, ' ', dm_mgmt_client.client_first_name) AS client_name,
                dm_mgmt_massage.massage_name,
                dm_mgmt_service.service_date,
                dm_mgmt_service.service_cashed_price,
                dm_mgmt_service.service_is_voucher
               FROM dm_mgmt_service
                 JOIN dm_mgmt_massage ON dm_mgmt_massage.massage_id = dm_mgmt_service.service_massage_id_id
                 JOIN dm_mgmt_client ON dm_mgmt_client.client_id = dm_mgmt_service.service_client_id_id;
            
            ALTER TABLE public.dm_mgmt_conso_service
                OWNER TO uvwwlizpxibjin;
            """,
            "DROP VIEW dm_mgmt_conso_service;"
        ),
    ]
