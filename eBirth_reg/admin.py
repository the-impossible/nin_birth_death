from django.contrib import admin

from eBirth_reg.models import (
    BirthRegistration,
    Gender,
    HospitalProfile,
)


class HospitalProfileAdmin(admin.ModelAdmin):

    list_display = ('hospital_name', 'hospital_address',
                    'user_id',)
    search_fields = ('hospital_name',)
    ordering = ('hospital_name',)
    raw_id_fields = ['user_id']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class BirthRegistrationAdmin(admin.ModelAdmin):

    list_display = ('user_id', 'child_name', 'father_name', 'mother_name', 'gender', 'weight', 'certificate_num')
    search_fields = ('hospital_id__hospital_name', 'user_id__email')
    ordering = ('child_name',)
    raw_id_fields = ['user_id', 'place_of_birth',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(HospitalProfile, HospitalProfileAdmin)
# admin.site.register(BirthRegistration, BirthRegistrationAdmin)
admin.site.register(Gender)
