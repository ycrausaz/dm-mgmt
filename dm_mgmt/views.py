from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

from .models import Client, Massage, Service, ConsoService
from .forms import ServiceForm, ClientForm, OutputServicesCSV

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from django.db import connection

#import logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

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

@login_required
def list_clients(request):
#    client_list = Client.objects.all()
    p = Paginator(Client.objects.all(), 20)
    page = request.GET.get('page')
    clients = p.get_page(page)
#    return render(request, 'clients/list_clients.html', {'client_list': client_list})
    return render(request, 'clients/list_clients.html', {'clients': clients})

@login_required
def list_massages(request):
#    massage_list = Massage.objects.all()
    p = Paginator(Massage.objects.all(), 20)
    page = request.GET.get('page')
    massages = p.get_page(page)
#    return render(request, 'massages/list_massages.html', {'massage_list': massage_list})
    return render(request, 'massages/list_massages.html', {'massages': massages})

@login_required
def list_services(request):
#    service_list = Service.objects.all()
    p = Paginator(Service.objects.all(), 20)
    page = request.GET.get('page')
    services = p.get_page(page)
#    return render(request, 'services/list_services.html', {'service_list': service_list})
    return render(request, 'services/list_services.html', {'services': services})

@login_required
def add_client(request):
    submitted = False
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_client?submitted=True')
    else:
        form = ClientForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'clients/add_client.html', {'form': form, 'submitted': submitted})

@login_required
def add_massage(request):
    return render(request, 'tbd.html')

#@login_required
def add_service(request):
    submitted = False
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_service?submitted=True')
    else:
        form = ServiceForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'services/add_service.html', {'form': form, 'submitted': submitted})

@login_required
def show_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
#    query = "select massage_name, service_date from dm_mgmt_service join dm_mgmt_massage on dm_mgmt_service.service_massage_id_id = dm_mgmt_massage.massage_id and dm_mgmt_service.service_client_id_id = " + str(client_id) + " order by dm_mgmt_service.service_date desc"
#    with connection.cursor() as cursor:
#        cursor.execute(query)
#        #https://stackoverflow.com/questions/14264485/django-format-raw-query-for-template-when-using-cursor-execute
#        results = cursor.fetchall()
#        massages_count = len(results)
#        x = cursor.description
#        massages = []
#        for r in results:
#            i = 0
#            d = {}
#            while i < len(x):
#                d[x[i][0]] = r[i]
#                i = i + 1
#            massages.append(d)
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
        response['Content-Disposition'] = 'attachment; filename=prestations.csv'
        
        writer = csv.writer(response)
    
        services = Service.objects.all()
    
        writer.writerow(['Client', 'Massage', 'Date', 'Montant encaissé'])
        
        for service in services:
            writer.writerow([service.service_client_id_id, service.service_massage_id_id, service.service_date, service.service_cashed_price])
        
        return response
    else:
        form = OutputServicesCSV
        return render(request, 'outputs/output_service_csv.html', {'form': form})

@login_required
def output_service_pdf(request):
    return render(request, 'outputs/output_service_pdf.html')

@login_required
def output_client_csv(request):
    return render(request, 'outputs/output_client_csv.html')

@login_required
def output_client_pdf(request):
    return render(request, 'outputs/output_client_pdf.html')
