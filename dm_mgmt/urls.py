from django.views.i18n import JavaScriptCatalog
from django.urls import include
from django.urls import path
from . import views
from .views import AddClientView, AddServiceView, ListServicesView, ListMassagesView, ListClientsView, DeleteServiceView, ShowClientView, ShowServiceView, UpdateClientView, UpdateServiceView, OutputServicesView, OutputClientsCSV, OutputAllClientsCSV, UserLogin, UserLogout
from django.contrib.auth.decorators import login_required

# urlpatterns += [
#     path('mgmt/', include('mgmt.urls')),
# ]

urlpatterns = [
    path('', include('pwa.urls')),
    path(r'', views.home, name='home'),
    path('list_clients', login_required(ListClientsView.as_view()), name='list-clients'),
    path('list_massages', login_required(ListMassagesView.as_view()), name='list-massages'),
    path('list_services', login_required(ListServicesView.as_view()), name='list-services'),
    path('add_client', login_required(AddClientView.as_view()), name='add-client'),
    path('add_massage', views.add_massage, name='add-massage'),
    path('add_service', login_required(AddServiceView.as_view()), name='add-service'),
#    path('delete_service/<int:pk>', login_required(DeleteServiceView.as_view()), name='delete-service'),
    path('show_client/<int:pk>', login_required(ShowClientView.as_view()), name='show-client'),
    path('show_service/<int:pk>', login_required(ShowServiceView.as_view()), name='show-service'),
    path('update_client/<int:pk>', login_required(UpdateClientView.as_view()), name='update-client'),
    path('update_service/<int:pk>', login_required(UpdateServiceView.as_view()), name='update-service'),
    path('output_services_csv', login_required(OutputServicesView.as_view()), name='output-services-csv'),
    path('output_all_clients_csv', login_required(OutputAllClientsCSV.as_view()), name='output-all-clients-csv'),
    path('output_clients_csv', login_required(OutputClientsCSV.as_view()), name='output-clients-csv'),
    path('login_user', UserLogin.as_view(), name='login-user'),
    path('logout_user', UserLogout.as_view(), name='logout-user'),

    # TO BE REPLACED BY THE CBV VERSION ASAP!!!
    path('delete_service/<service_id>', views.delete_service, name='delete-service'),
]
