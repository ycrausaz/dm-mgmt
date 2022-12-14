from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

# Create your views here.

from .models import Client, Massage, Service, ConsoService
from .forms import ServiceForm, ClientForm, DateChooserFromToForm

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from django.db import connection
from datetime import datetime

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib import colors
import json

import pandas as pd

import calendar
from django.utils import translation
from django.utils.translation import gettext as _
translation.activate('fr')


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def home(request):
    # """View function for home page of site."""
    #
    # # Generate counts of some of the main objects
    # # num_books = Book.objects.all().count()
    # num_clients = Client.objects.all().count()
    # # num_instances = BookInstance.objects.all().count()
    # num_massages = Massage.objects.all().count()
    #
    # # Available books (status = 'a')
    # # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # num_clients_yann = 0 #Client.objects.filter(client_first_name__icontains='yann').count()
    #
    # # The 'all()' is implied by default.
    # # num_authors = Author.objects.count()
    # num_services = Service.objects.all().count()
    #
    # context = {
    #     'num_clients': num_clients,
    #     'num_massages': num_massages,
    #     'num_services': num_services,
    #     'num_clients_yann': num_clients_yann,
    # }

    # Render the HTML template index.html with the data in the context variable
   return redirect('add-service')
#    return render(request, 'home.html')#, context=context)

class ListClientsView(ListView):
    model = Client
    template_name = 'clients/list_clients.html'
    context_object_name = 'clients'
    paginate_by = 20

class ListMassagesView(ListView):
    model = Massage
    template_name = 'massages/list_massages.html'
    context_object_name = 'massages'

class ListServicesView(ListView):
    model = Service
    template_name = 'services/list_services.html'
    context_object_name = 'services'
    paginate_by = 20

class AddClientView(SuccessMessageMixin, CreateView):
    model = Client
    template_name = 'clients/add_client.html'
    form_class = ClientForm
    success_url = reverse_lazy('list-clients')
    success_message = "Le client a ??t?? ajout?? avec succ??s."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        client_str = self.object.client_last_name + ' ' + self.object.client_first_name
        return 'L\'ajout de "' + client_str + '" a ??t?? r??alis?? avec succ??s.'

@login_required
def add_massage(request):
    return render(request, 'tbd.html')

class AddServiceView(SuccessMessageMixin, CreateView):
    model = Service
    template_name = 'services/add_service.html'
    form_class = ServiceForm
    success_url = reverse_lazy('add-service')
    success_message = "Le service a ??t?? ajout?? avec succ??s."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["json_massage_is_voucher"] = json.dumps(list(Massage.objects.values_list('massage_id', 'massage_is_voucher')))
        context["json_massage_price"] = json.dumps(list(Massage.objects.values_list('massage_id', 'massage_price')))
        context["json_massage_duration"] = json.dumps(list(Massage.objects.values_list('massage_id', 'massage_duration')))
        return context

    def get_success_message(self, cleaned_data):
        return 'L\'ajout de "' + str(self.object.service_client_id) + ' => ' + str(self.object.service_massage_id) + '" a ??t?? r??alis?? avec succ??s.'

class DeleteServiceView(SuccessMessageMixin, DeleteView):
    pass
#    model = Service
#    template_name = 'services/delete_service.html'
#    form_class = ServiceForm
#    success_url = reverse_lazy('list-services')
#    success_message = "Le service a ??t?? supprim?? avec succ??s."
#
#    def form_valid(self, form):
#        print(">>>>>>>>>>>>>>> form_valid")
#        return super().form_valid(form)
#
#    def form_invalid(self, form):
#        print("*************** form_invalid")
#        return super().form_invalid(form)

def delete_service(request, service_id): # TO BE REPLACED BY THE CBV VERSION ASAP!!!
    service = Service.objects.get(pk=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('list-services')
    return render(request, 'services/delete_service.html', {'service': service})

class ShowClientView(DetailView):
    model = Client
    template_name = 'clients/show_client.html'
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = Client.objects.get(pk=self.kwargs['pk'])
        conso_service = ConsoService.objects.filter(client_id__exact=client.client_id)
        context['client'] = client
        context['massages'] = conso_service
        return context

class ShowServiceView(DetailView):
    model = Service
    template_name = 'services/show_service.html'
    form_class = ServiceForm

class UpdateClientView (SuccessMessageMixin, UpdateView):
    model = Client
    template_name = 'clients/update_client.html'
    form_class = ClientForm
    success_url = reverse_lazy('list-clients')
    success_message = 'Les informations du client ont ??t?? mises ?? jour avec succ??s.'

class UpdateServiceView (SuccessMessageMixin, UpdateView):
    model = Service
    template_name = 'services/update_service.html'
    form_class = ServiceForm
    success_url = reverse_lazy('list-services')
    success_message = 'Les informations du service on ??t?? mises ?? jour avec succ??s.'

class OutputServicesView(View):
    def get(self, request, *args, **kwargs):
        form = DateChooserFromToForm()
        return render(request, 'outputs/output_services_csv.html', {'form': form})

    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        min_date = request.POST['min_date']
#        logger.info("************* min_date = " + min_date)
        min_date_str = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y%m%d")
        max_date = request.POST['max_date']
#        logger.info("************* max_date = " + max_date)
        max_date_str = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y%m%d")
        filename = "prestations-" + min_date_str + "-" + max_date_str
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        
        writer = csv.writer(response)
        
        min_date = request.POST['min_date']
        max_date = request.POST['max_date']

        min_date = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        max_date = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y-%m-%d")

#        logger.info(min_date)
#        logger.info(max_date)
    
        services = ConsoService.objects.filter(service_date__range=(min_date, max_date))
    
        writer.writerow(['Client', 'Massage', 'Date', 'Montant encaiss??', 'Bon fait valoir'])
        
        for service in services:
            writer.writerow([service.client_name, service.massage_name, service.service_date, service.service_cashed_price, service.service_is_voucher])
        
        return response
       
#@login_required
#def output_service_pdf(request):
#    if request.method == "POST":
#        response = HttpResponse(content_type='application/pdf')
#        min_date = request.POST['min_date']
#        min_date_str = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y%m%d")
#        min_date_query = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y-%m-%d")
#        max_date = request.POST['max_date']
#        max_date_str = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y%m%d")
#        max_date_query = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y-%m-%d")
#        filename = "prestations-" + min_date_str + "-" + max_date_str
#        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
#
#        width, height = A4
#        styles = getSampleStyleSheet()
#        styleN = styles["BodyText"]
#        styleN.alignment = TA_LEFT
#        styleBH = styles["Normal"]
#        styleBH.alignment = TA_CENTER
#    
#        def coord(x, y, unit=1):
#            x, y = x * unit, height - y * unit
#            return x, y
#    
#        inspection = Paragraph('''<b>Inspection Id</b>''', styleBH)
#        licplt = Paragraph('''<b>Licence Plate</b>''', styleBH)
#        imgs = Paragraph('''<b>Images</b>''', styleBH)
#        cmnts = Paragraph('''<b>Comments</b>''', styleBH)
#    
#        buffer = io.BytesIO()
#    
#        p = canvas.Canvas(buffer, pagesize=A4)
#    
#        p.drawString(20, 800, "Prestations entre le " + min_date + " et le " + max_date)
#    
#        services = ConsoService.objects.filter(service_date__range=(min_date_query, max_date_query))
#        data = [['Client', 'Massage', 'Date', 'Montant encaiss??', 'Bon fait valoir']]
#        try:
#            for service in services:
#                row = []
#                row.append(service.client_name)
#                row.append(service.massage_name)
#                row.append(service.service_date)
#                row.append(service.service_cashed_price)
#                row.append(service.service_is_voucher)
#                data.append(row)
#        except:
#            pass
#        table = Table(data, colWidths=[4 * cm, 4 * cm, 5 * cm, 4 * cm])
#    
#        table.setStyle(TableStyle([
#            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
#        ]))
#        table.wrapOn(p, width, height)
#        table.wrapOn(p, width, height)
#        table.drawOn(p, *coord(1.8, 9.6, cm))
#        p.showPage()
#        p.save()
#        pdf = buffer.getvalue()
#        buffer.close()
#        response.write(pdf)
#        return response
#
#    else:
#        form = DateChooserFromToForm()
#        return render(request, 'outputs/output_service_pdf.html', {'form': form})

class OutputAllClientsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        date_str = datetime.now().strftime("%Y%m%d")
        filename = "clients_total-" + date_str
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        
        writer = csv.writer(response)
        
        clients = Client.objects.all()
    
        writer.writerow(['Nom', 'Pr??nom', 'Date de naissance', 'Addresse', 'Compl??ment d\'adresse', 'NPA', 'Localit??', 'T??l??phone 1', 'T??l??phone 2', 'E-mail'])
        
        for client in clients:
            writer.writerow([client.client_last_name, client.client_first_name, client.client_birthdate, client.client_address, client.client_additional_address, client.client_zip_code, client.client_city, client.client_phone_number_1, client.client_phone_number_2, client.client_email_address])
        return response

class OutputClientsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        date_str = datetime.now().strftime("%Y%m%d")
        filename = "clients_actifs-" + date_str
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        
        writer = csv.writer(response)
        
        clients = Client.objects.filter(client_is_displayed=True)
    
        writer.writerow(['Nom', 'Pr??nom', 'Date de naissance', 'Addresse', 'Compl??ment d\'adresse', 'NPA', 'Localit??', 'T??l??phone 1', 'T??l??phone 2', 'E-mail'])
        
        for client in clients:
            writer.writerow([client.client_last_name, client.client_first_name, client.client_birthdate, client.client_address, client.client_additional_address, client.client_zip_code, client.client_city, client.client_phone_number_1, client.client_phone_number_2, client.client_email_address])
        return response

class StatsView(View):
    def get(self, request, *args, **kwargs):
        form = DateChooserFromToForm()
        return render(request, 'stats/stats_get_dates.html', {'form': form})

    def post(self, request, *args, **kwargs):
        min_date = request.POST['min_date']
        max_date = request.POST['max_date']

        min_date_sql = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        max_date_sql = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y-%m-%d")

        services = ConsoService.objects.filter(service_date__range=(min_date_sql, max_date_sql)).values()
        df = pd.DataFrame(services)
        df['client_gender'] = df['client_gender'].astype('category').cat.codes
        df['weekday'] = df['service_date'].apply(lambda x: _(calendar.day_name[x.weekday()]).capitalize())
        df['service_cashed_price'] = df['service_cashed_price'].astype(float)
        df_init = df.copy()

        nb_m = len(df[df['client_gender']==1])
        nb_f = len(df[df['client_gender']==0])
        nb_total = nb_f + nb_m
        total_h = df['service_duration'].sum()/60
        total_chf = df['service_cashed_price'].sum()

        df = df[['client_id', 'client_name', 'service_cashed_price']].groupby(['client_id', 'client_name'], as_index=False).sum().sort_values(['service_cashed_price'])
        
        top_clients_10 = df.nlargest(10, 'service_cashed_price')[['client_id', 'client_name', 'service_cashed_price']]
        top_clients_10_dict = []
        for i, row in top_clients_10.iterrows():
            top_clients_10_dict.append({
                'client_id': row['client_id'], 
                'client_name': row['client_name'],
                'service_cashed_price': row['service_cashed_price']
            })

        df = df_init.copy()
        df = df[~(df[df.columns[4]].str.match("abo.*", case=False) | df[df.columns[4]].str.match("bon.*", case=False))]
        top_massages_10 = df[['service_id', 'massage_name', 'service_duration']].groupby(['massage_name'], as_index=False).sum().sort_values(['service_duration'])
        top_massages_10 = top_massages_10.nlargest(10, 'service_duration')[['service_id', 'massage_name', 'service_duration']]
        top_massages_10_dict = []
        for i, row in top_massages_10.iterrows():
            top_massages_10_dict.append({
                'service_id': row['service_id'], 
                'massage_name': row['massage_name'],
                'service_duration': row['service_duration']/60
            })


        df = df_init.copy()
        df = df[['service_id', 'weekday', 'service_duration']].groupby(['weekday'], as_index=False).sum().sort_values(['service_duration'])
        top_days_3 = df.nlargest(3, 'service_duration')[['service_id', 'weekday', 'service_duration']]
        top_days_3_dict = []
        for i, row in top_days_3.iterrows():
            top_days_3_dict.append({
                'service_id': row['service_id'], 
                'weekday': row['weekday'],
                'service_duration': row['service_duration']/60
            })


        context = {
            'min_date': min_date,
            'max_date': max_date,
            'nb_total': nb_total,
            'nb_f': nb_f,
            'nb_m': nb_m,
            'total_h': total_h,
            'total_chf': total_chf,
            'top_clients_10': top_clients_10_dict,
            'top_massages_10': top_massages_10_dict,
            'top_days_3': top_days_3_dict,
            'df': df_init.to_html(),
        }

        return render(request, 'stats/stats.html', context)

class UserLogin(View):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add-service')
        else:
            messages.success(request, ("Erreur dans le login"))
            return redirect('login-user')

    def get(self, request, *args, **kwargs):
        return render(request, 'login_user.html', {})

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login-user')
