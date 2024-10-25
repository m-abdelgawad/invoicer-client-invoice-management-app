from django.urls import path
from . import views


app_name = 'invoicer'

urlpatterns = [
    path('', views.home, name='home'),
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/view/<slug:client_slug>/', views.read_client, name='read_client'),
    path('clients/update/<slug:client_slug>/', views.update_client, name='update_client'),
    path('clients/delete/<slug:client_slug>/', views.delete_client, name='delete_client'),
    path('invoices/', views.invoices_list, name='invoices_list'),
    # The error message suggests that the read_invoice view is being called
    # instead of the create_invoice view when you try to add a new invoice.
    # This is because the URL pattern apps/invoicer/invoices/<slug:invoice_slug>/
    # matches the URL apps/invoicer/invoices/add_invoice/, and Django thinks that
    # "add_invoice" is a value for the invoice_slug parameter in the URL.
    path('invoices/add_invoice/', views.create_invoice, name='create_invoice'),
    path('invoices/view/<slug:invoice_slug>/', views.read_invoice, name='read_invoice'),
    path('invoices/update/<slug:invoice_slug>/', views.update_invoice, name='update_invoice'),
    path('invoices/delete/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('profile/', views.read_profile, name='read_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('invoices/export/<slug:invoice_slug>/', views.export_invoice, name='export_invoice'),
]
