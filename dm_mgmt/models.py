from datetime import datetime


from django.db import models, IntegrityError


# Create your models here.


class Client(models.Model):
    GENDER_CHOICES = {("M", "M"), ("F", "F")}
    client_id = models.AutoField(primary_key=True, unique=True)
    client_first_name = models.CharField('Prénom', max_length=80)
    client_last_name = models.CharField('Nom', max_length=80)
    client_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    client_birthdate = models.DateField('Date de naissance', null=True, blank=True)#, help_text="Format : jj.mm.aaaa (Exemple : 24.02.1980)")
    client_address = models.CharField('Adresse', null=True, blank=True, max_length=80)
    client_additional_address = models.CharField('Complément d\'adresse', null=True, blank=True, max_length=80)
    client_zip_code = models.PositiveSmallIntegerField('NPA', null=True, blank=True)
    client_city = models.CharField('Localité', null=True, blank=True, max_length=80)
    client_phone_number_1 = models.CharField('Téléphone 1', max_length=30)#, help_text="Format : +xx xx xxx xx xx (Exemple : +41 79 123 45 67)")
    client_phone_number_2 = models.CharField('Téléphone 2', max_length=30, null=True, blank=True)#, help_text="Format : +xx xx xxx xx xx (Exemple : +41 79 123 45 67)")
    client_email_address = models.EmailField('E-mail', null=True, blank=True)
    client_comment = models.TextField('Commentaire', null=True, blank=True)
    client_is_displayed = models.BooleanField('Client à prendre en compte', default=True)

    def __str__(self):
        ret = self.client_last_name + " " + self.client_first_name
        if not self.client_birthdate is None:
            ret += " (" + str(self.client_birthdate.strftime("%d.%m.%Y")) + ")"
        return ret

#    def save(self, *args, **kwargs):
#        print("Save 'Client'")
#        super(Client, self).save(*args, **kwargs)


    class Meta:
        ordering = ["client_last_name", "client_first_name"]


class Massage(models.Model):
    massage_id = models.AutoField(primary_key=True, unique=True)
    massage_name = models.CharField('Nom du massage', max_length=80)
    # massage_description = models.TextField('Description')
    massage_duration = models.PositiveSmallIntegerField('Durée (en minutes)')
    massage_price = models.FloatField('Prix')
    massage_is_available = models.BooleanField('Massage actuellement proposé', default=False)
    massage_is_voucher = models.BooleanField('Bon / Abo', default=False)
    massage_order = models.PositiveSmallIntegerField('Position', default=0)

    def __str__(self):
        return self.massage_name + " (" + str(self.massage_duration) + "’)"
#        if self.massage_is_available:
#            return self.massage_name + " - " + str(self.massage_duration) + " min."
#        else:
#            return self.massage_name + " - " + str(self.massage_duration) + " min. (pas dispo)"

    class Meta:
        ordering = ["massage_order"]


class Service(models.Model):
    service_id = models.AutoField(primary_key=True, unique=True)
    service_client_id = models.ForeignKey(Client, null=True, on_delete=models.DO_NOTHING, verbose_name="Client", limit_choices_to={'client_is_displayed': True})
    service_massage_id = models.ForeignKey(Massage, null=True, on_delete=models.DO_NOTHING, verbose_name="Massage", limit_choices_to={'massage_is_available': True})
    service_date = models.DateField('Date du massage')
    service_duration = models.PositiveSmallIntegerField('Durée du massage (en minutes)', blank=False, null=False, default=0)
    service_comment = models.TextField('Remarque', blank=True, null=True)
#    service_cashed_price = models.FloatField('Montant encaissé (CHF)')
    service_cashed_price = models.DecimalField('Montant encaissé (CHF)', max_digits=5, decimal_places=2)
    service_is_voucher = models.BooleanField('Bon / abonnement', blank=True, default=False)

    def __str__(self):
        return str(self.service_date.strftime("%d.%m.%Y")) + " : " + str(self.service_client_id) + " => " + str(self.service_massage_id)

#    def save(self, *args, **kwargs):
#        print("Save 'Service': " + str(self.service_client_id) + ", " + str(self.service_massage_id))
#        super(Service, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-service_date"]

    # @property
    # def service_theorical_price(self):
    #     # print(self.service_duration)
    #     # print(self.service_massage_id)
    #     return float(self.service_duration) # * self.service_massage_id.massage_price


class ConsoService(models.Model):
    client_id = models.IntegerField()
    client_name = models.CharField(max_length=255, primary_key=True)
    client_gender = models.CharField(max_length=1)
    massage_name = models.CharField(max_length=255)
    service_date = models.DateField()
    service_cashed_price = models.FloatField()
    service_is_voucher = models.BooleanField()

    class Meta:
        managed = False
        db_table = "dm_mgmt_conso_service"
        ordering = ["-service_date"]
