# My django imports
from django import forms

# My app imports
from eBirth_reg.models import (
    BirthRegistration,
    DeathRegistration,
    Gender,
    HospitalProfile,
)


class BirthRegistrationForm(forms.ModelForm):

    child_name = forms.CharField(help_text='Enter Child name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    father_name = forms.CharField(help_text='Enter Father name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    mother_name = forms.CharField(help_text='Enter Mother name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    weight = forms.CharField(help_text='Enter child birth weight', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'number',
            'step': 'any',
        }
    ))

    date_time = forms.CharField(help_text='Birth date and time', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }
    ))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Select Child Gender", required=True, help_text="Select child's gender", widget=forms.Select(
        attrs={
            'class': 'form-control select form-select',
        }
    ))

    class Meta:
        model = BirthRegistration
        fields = ('child_name', 'father_name', 'mother_name',
                  'date_time', 'weight', 'gender')


class DeathRegistrationForm(forms.ModelForm):

    date_of_death = forms.CharField(help_text='Death Date and Time', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }
    ))

    place_of_death = forms.CharField(help_text='Enter place of death', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    address_of_deceased = forms.CharField(help_text='Enter the address of deceased', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    class Meta:
        model = DeathRegistration
        fields = ('date_of_death', 'place_of_death', 'address_of_deceased', )


class HospitalProfileForm(forms.ModelForm):

    hospital_name = forms.CharField(help_text='Enter Hospital Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    hospital_address = forms.CharField(help_text='Enter Hospital Address', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    # signature = forms.ImageField(required=False, widget=forms.FileInput(
    #     attrs={
    #             'class':'form-control',
    #             'type':'file',
    #             'accept':'image/png, image/jpeg'
    #         }
    #     ))

    class Meta:
        model = HospitalProfile
        fields = ('hospital_name', 'hospital_address',)
