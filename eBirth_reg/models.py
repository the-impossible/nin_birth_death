from django.db import models
import uuid
from django.shortcuts import reverse

# My app imports
from eBirth_auth.models import (
    User
)

# Create your models here.


class HospitalProfile(models.Model):
    hospital_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    hospital_address = models.CharField(max_length=500)
    signature = models.ImageField(null=True, blank=True, upload_to='uploads/')

    def __str__(self):
        return self.hospital_name

    def get_absolute_url(self):
        return reverse("reg:hospital_profile", kwargs={
            'pk': self.user_id.user_id
        })

    class Meta:
        db_table = 'Hospital Profile'
        verbose_name_plural = 'Hospital Profile'


class Gender(models.Model):
    gender_title = models.CharField(max_length=7)

    def __str__(self):
        return self.gender_title

    class Meta:
        db_table = 'Gender'
        verbose_name_plural = 'Gender'


class HospitalAdminProfile(models.Model):
    admin_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(
        to=HospitalProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        db_table = 'Hospital Admin Profile'
        verbose_name_plural = 'Hospital Admin Profile'


class BirthRegistration(models.Model):

    birth_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    weight = models.CharField(max_length=10)
    place_of_birth = models.ForeignKey(
        to=HospitalProfile, on_delete=models.CASCADE)
    gender = models.ForeignKey(to=Gender, on_delete=models.CASCADE)
    certificate_num = models.CharField(max_length=10)
    date_issue = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child_name} : {self.certificate_num}"

    def get_fullname(self):
        return f"{self.child_name} {self.father_name}"

    class Meta:
        db_table = 'Birth Registration'
        verbose_name_plural = 'Birth Registrations'


class DeathRegistration(models.Model):

    death_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    birth_id = models.ForeignKey(to=BirthRegistration, on_delete=models.CASCADE)
    date_of_death = models.DateTimeField()
    age_at_death = models.CharField(max_length=4)
    place_of_death = models.CharField(max_length=100)
    address_of_deceased = models.CharField(max_length=100)
    certificate_num = models.CharField(max_length=10)
    hospital_issued = models.ForeignKey(
        to=HospitalProfile, on_delete=models.CASCADE)
    date_issue = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_age(self):
        try:
            birth = BirthRegistration.objects.get(
                user_id=self.user_id).date_time.year

            death = self.date_of_death.year

            self.age_at_death = death - birth

            return self.age_at_death

        except:
            self.age_at_death = "None"

            return self.age_at_death

    def __str__(self):
        return f"{self.user_id} : {self.certificate_num}"

    class Meta:
        db_table = 'Death Registration'
        verbose_name_plural = 'Death Registrations'
