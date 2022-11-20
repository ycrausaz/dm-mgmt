from django import forms
from django.forms import ModelForm
from .models import Client, Massage, Service
from django.contrib.admin import widgets

class MassageForm(ModelForm):
    class Meta:
        model = Massage
        fields = ['massage_name', 'massage_duration', 'massage_price']

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_client_id', 'service_date', 'service_massage_id', 'service_cashed_price']
        # labels = {
        #     'service_client_id': '',
        #     'service_massage_id': '',
        #     'service_date': '',
        #     'service_duration': '',
        #     'service_comment': '',
        #     'service_cashed_price': '',
        # }
        widgets = {
            'service_client_id': forms.Select(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Nom du client'}),
             'service_massage_id': forms.Select(attrs={'class':'form-control', 'style':'width: 300px;', 'onchange': "updatePrice();"}),#, 'placeholder':'Nom du massage'}),
             'service_date': widgets.AdminDateWidget(attrs={'placeholder':'jj.mm.aaaa'}),
             'service_duration': forms.NumberInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Durée de la prestation'}),
            'service_comment': forms.Textarea(attrs={'class':'form-control', 'rows':5}),
             'service_cashed_price': forms.NumberInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Prix encaissé'}),
         }

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['client_last_name', 'client_first_name', 'client_birthdate', 'client_address', 'client_additional_address', 'client_zip_code', 'client_city', 'client_phone_number_1', 'client_phone_number_2', 'client_email_address', 'client_comment']
        widgets = {
            'client_last_name': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Nom'}),
            'client_first_name': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Prénom'}),
            'client_birthdate': forms.TextInput(attrs={'class':'form-control', 'style':'width:300px;', 'placeholder':'jj.mm.aaaa'}),
#            'client_birthdate': widgets.AdminDateWidget(attrs={'placeholder':'jj.mm.aaaa'}),
            'client_address': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Adresse'}),
            'client_additional_address': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Complément d\'adresse'}),
            'client_zip_code': forms.NumberInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'NPA'}),
            'client_city': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Localité'}),
            'client_phone_number_1': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Téléphone 1'}),
            'client_phone_number_2': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'Téléphone 2'}),
            'client_email_address': forms.TextInput(attrs={'class':'form-control', 'style':'width: 300px;'}),#, 'placeholder':'E-mail'}),
            'client_comment': forms.Textarea(attrs={'class':'form-control', 'rows':5, 'style':'width: 300px;'})
        }

#class ClientFormReadonly(ClientForm):

class OutputServicesCSV(forms.Form):
    min_date = forms.TextInput(attrs={'class':'form-control', 'style':'width:300px;', 'placeholder':'jj.mm.aaaa'}),
    max_date = forms.TextInput(attrs={'class':'form-control', 'style':'width:300px;', 'placeholder':'jj.mm.aaaa'})
    
    class Meta:
        fields = ['min_date', 'max_date']
