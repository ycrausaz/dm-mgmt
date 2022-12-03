from django.views.i18n import JavaScriptCatalog
from django.urls import include
from django.urls import path
from . import views
from .views import AddClientView, AddServiceView
from django.contrib.auth.decorators import login_required

# urlpatterns += [
#     path('mgmt/', include('mgmt.urls')),
# ]

urlpatterns = [
    path('', views.home, name='home'),
    path('list_clients', views.list_clients, name='list-clients'),
    path('list_massages', views.list_massages, name='list-massages'),
    path('list_services', views.list_services, name='list-services'),
#    path('add_client', views.add_client, name='add-client'),
    path('add_client', login_required(AddClientView.as_view()), name='add-client'),
    path('add_massage', views.add_massage, name='add-massage'),
#    path('add_service', views.add_service, name='add-service'),
    path('add_service', login_required(AddServiceView.as_view()), name='add-service'),
    path('show_client/<int:client_id>', views.show_client, name='show-client'),
    path('update_client/<int:client_id>', views.update_client, name='update-client'),
    path('update_service/<int:service_id>', views.update_service, name='update-service'),
    path('output_client_csv', views.output_client_csv, name='output-client-csv'),
    path('output_client_pdf', views.output_client_pdf, name='output-client-pdf'),
    path('output_service_csv', views.output_service_csv, name='output-service-csv'),
    path('output_service_pdf', views.output_service_pdf, name='output-service-pdf'),
    path('login_user', views.login_user, name='login-user'),
    path('logout_user', views.logout_user, name='logout-user'),
#    path('tbd', views.tbd, name='tbd'),
#    path('jsi18n', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
