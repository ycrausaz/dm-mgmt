from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic.edit import CreateView
from django.views.generic import ListView

from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

from .models import Client, Massage, Service, ConsoService
from .forms import ServiceForm, ClientForm, OutputServices

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

#@login_required
#def list_clients(request):
##    client_list = Client.objects.all()
#    p = Paginator(Client.objects.all(), 20)
#    page = request.GET.get('page')
#    clients = p.get_page(page)
##    return render(request, 'clients/list_clients.html', {'client_list': client_list})
#    return render(request, 'clients/list_clients.html', {'clients': clients})
class ListClientsView(ListView):
    model = Client
    template_name = 'clients/list_clients.html'
    context_object_name = 'clients'
    paginate_by = 20

#@login_required
#def list_massages(request):
##    massage_list = Massage.objects.all()
#    p = Paginator(Massage.objects.all(), 20)
#    page = request.GET.get('page')
#    massages = p.get_page(page)
##    return render(request, 'massages/list_massages.html', {'massage_list': massage_list})
#    return render(request, 'massages/list_massages.html', {'massages': massages})
class ListMassagesView(ListView):
    model = Massage
    template_name = 'massages/list_massages.html'
    context_object_name = 'massages'

#@login_required
#def list_services(request):
##    service_list = Service.objects.all()
#    p = Paginator(Service.objects.all(), 20)
#    page = request.GET.get('page')
#    services = p.get_page(page)
##    return render(request, 'services/list_services.html', {'service_list': service_list})
#    return render(request, 'services/list_services.html', {'services': services})
class ListServicesView(ListView):
    model = Service
    template_name = 'services/list_services.html'
    context_object_name = 'services'
    paginate_by = 20

class AddClientView(SuccessMessageMixin, CreateView):
    model = Client
    template_name = 'clients/add_client.html'
    form_class = ClientForm
    success_url = 'add_client'
    success_message = "Le client a été ajouté."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@login_required
def add_massage(request):
    return render(request, 'tbd.html')

class AddServiceView(SuccessMessageMixin, CreateView):
    model = Service
    template_name = 'services/add_service.html'
    form_class = ServiceForm
    success_url = 'add_service'
    success_message = "Le service a été ajouté."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["json_massage_is_voucher"] = json.dumps(list(Massage.objects.values_list('massage_id', 'massage_is_voucher')))
        context["json_massage_price"] = json.dumps(list(Massage.objects.values_list('massage_id', 'massage_price')))
        return context

@login_required
def show_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    conso_service = ConsoService.objects.filter(client_id__exact=client_id)
    return render(request, 'clients/show_client.html', {'client': client, 'form': form, 'massages': conso_service})

@login_required
def update_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('list-clients')
    return render(request, 'clients/update_client.html', {'client': client, 'form': form})

@login_required
def update_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('list-services')
    return render(request, 'services/update_service.html', {'service': service, 'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add-service')
        else:
            messages.success(request, ("Erreur dans le login"))
            return redirect('login-user')
    else:
        return render(request, 'login_user.html', {})

def logout_user(request):
    logout(request)
    return redirect('login-user')

@login_required
def output_service_csv(request):
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        min_date = request.POST['min_date']
        logger.info("************* min_date = " + min_date)
        min_date_str = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y%m%d")
        max_date = request.POST['max_date']
        logger.info("************* max_date = " + max_date)
        max_date_str = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y%m%d")
        filename = "prestations-" + min_date_str + "-" + max_date_str
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        
        writer = csv.writer(response)
        
        min_date = request.POST['min_date']
        max_date = request.POST['max_date']

        min_date = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        max_date = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y-%m-%d")

        logger.info(min_date)
        logger.info(max_date)
    
        services = ConsoService.objects.filter(service_date__range=(min_date, max_date))
    
        writer.writerow(['Client', 'Massage', 'Date', 'Montant encaissé', 'Bon fait valoir'])
        
        for service in services:
            writer.writerow([service.client_name, service.massage_name, service.service_date, service.service_cashed_price, service.service_is_voucher])
        
        return response
    else:
        form = OutputServices()
        return render(request, 'outputs/output_service_csv.html', {'form': form})

@login_required
def output_service_pdf(request):
    if request.method == "POST":
        response = HttpResponse(content_type='application/pdf')
        min_date = request.POST['min_date']
        min_date_str = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y%m%d")
        min_date_query = datetime.strptime(min_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        max_date = request.POST['max_date']
        max_date_str = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y%m%d")
        max_date_query = datetime.strptime(max_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        filename = "prestations-" + min_date_str + "-" + max_date_str
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
    
        def coord(x, y, unit=1):
            x, y = x * unit, height - y * unit
            return x, y
    
        inspection = Paragraph('''<b>Inspection Id</b>''', styleBH)
        licplt = Paragraph('''<b>Licence Plate</b>''', styleBH)
        imgs = Paragraph('''<b>Images</b>''', styleBH)
        cmnts = Paragraph('''<b>Comments</b>''', styleBH)
    
        buffer = io.BytesIO()
    
        p = canvas.Canvas(buffer, pagesize=A4)
    
        p.drawString(20, 800, "Prestations entre le " + min_date + " et le " + max_date)
    
        services = ConsoService.objects.filter(service_date__range=(min_date_query, max_date_query))
        data = [['Client', 'Massage', 'Date', 'Montant encaissé', 'Bon fait valoir']]
        try:
            for service in services:
                row = []
                row.append(service.client_name)
                row.append(service.massage_name)
                row.append(service.service_date)
                row.append(service.service_cashed_price)
                row.append(service.service_is_voucher)
                data.append(row)
        except:
            pass
        table = Table(data, colWidths=[4 * cm, 4 * cm, 5 * cm, 4 * cm])
    
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        table.wrapOn(p, width, height)
        table.wrapOn(p, width, height)
        table.drawOn(p, *coord(1.8, 9.6, cm))
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        form = OutputServices()
        return render(request, 'outputs/output_service_pdf.html', {'form': form})

@login_required
def output_client_csv(request):
    return render(request, 'outputs/output_client_csv.html')

@login_required
def output_client_pdf(request):
    return render(request, 'outputs/output_client_pdf.html')