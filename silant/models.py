from django.db import models

class Booktechnic(models.Model):
    model_technic_name = models.CharField(max_length=200)
    model_technic_desc = models.TextField()

    def __str__(self):
        return self.model_technic_name

class Bookengine(models.Model):
    model_engine_name = models.CharField(max_length=200)
    model_engine_desc = models.TextField()

    def __str__(self):
        return self.model_engine_name

class Bookclutch(models.Model):
    model_clutch_name = models.CharField(max_length=200)
    model_clutch_desc = models.TextField()

    def __str__(self):
        return self.model_clutch_name

class Bookaxle(models.Model):
    model_axle_name = models.CharField(max_length=200)
    model_axle_desc = models.TextField()

    def __str__(self):
        return self.model_axle_name

class Bookbridge(models.Model):
    model_bridge_name = models.CharField(max_length=200)
    model_bridge_desc = models.TextField()

    def __str__(self):
        return self.model_bridge_name

class Bookcompanies(models.Model):
    model_company_name = models.CharField(max_length=200)
    model_company_desc = models.TextField()

    def __str__(self):
        return self.model_company_name

class Booktm(models.Model):
    model_tm_name = models.CharField(max_length=200)
    model_tm_desc = models.TextField()

    def __str__(self):
        return self.model_tm_name

class Bookclaimpart(models.Model):
    model_claimpart_name = models.CharField(max_length=200)
    model_claimpart_desc = models.TextField()

    def __str__(self):
        return self.model_claimpart_name

class Bookclaimrecover(models.Model):
    model_claimrecover_name = models.CharField(max_length=200)
    model_claimrecover_desc = models.TextField()

    def __str__(self):
        return self.model_claimrecover_name



class Car(models.Model):
    factory_number = models.CharField(max_length=200, unique=True)
    model_technic = models.ForeignKey(Booktechnic, default=None, null=True, on_delete=models.SET_NULL)
    model_engine = models.ForeignKey(Bookengine, default=None, null=True, on_delete=models.SET_NULL)
    engine_factory_number = models.CharField(max_length=200)
    model_clutch = models.ForeignKey(Bookclutch, default=None, null=True, on_delete=models.SET_NULL)
    clutch_factory_number = models.CharField(max_length=200)
    driven_axle_model = models.ForeignKey(Bookaxle, default=None, null=True, on_delete=models.SET_NULL)
    driven_axle_factory_number = models.CharField(max_length=200)
    managed_bridge_model = models.ForeignKey(Bookbridge, default=None, null=True, on_delete=models.SET_NULL)
    managed_bridge_factory_number = models.CharField(max_length=200)
    agreement_number = models.CharField(max_length=200)
    agreement_date = models.DateField()
    receiver = models.CharField(max_length=300)
    receiver_address = models.CharField(max_length=300)
    configuration = models.CharField(max_length=400)
    client_name = models.CharField(max_length=200)
    service_company = models.ForeignKey(Bookcompanies, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.factory_number

class Technicalmaintenance(models.Model):
    tm_type = models.ForeignKey(Booktm, default=None, null=True, on_delete=models.SET_NULL)
    tm_date = models.DateField()
    tm_hours = models.IntegerField()
    tm_number = models.CharField(max_length=200)
    tm_number_date = models.DateField()
    tm_service_company = models.ForeignKey(Bookcompanies, default=None, null=True, on_delete=models.SET_NULL)
    tm_car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.tm_number

class Claimservice(models.Model):
    claim_date = models.DateField()
    claim_hours = models.IntegerField()
    claim_part = models.ForeignKey(Bookclaimpart, default=None, null=True, on_delete=models.SET_NULL)
    claim_description = models.TextField()
    claim_recover = models.ForeignKey(Bookclaimrecover, default=None, null=True, on_delete=models.SET_NULL)
    claim_used_parts = models.TextField(null=True, blank=True)
    claim_finish_date = models.DateField()
    claim_downtime = models.IntegerField()
    claim_service_company = models.ForeignKey(Bookcompanies, default=None, null=True, on_delete=models.SET_NULL)
    claim_car = models.ForeignKey(Car, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.claim_description










