from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Invoice, Service, Profile
from .forms import ClientForm, InvoiceForm, ServiceForm, ProfileForm
from django.forms import formset_factory, modelformset_factory
from django.db import transaction


def home(request):
    context = {}
    return render(request, 'invoicer/home.html', context)


# Create your views here.
@login_required
def clients_list(request):
    clients = Client.objects.filter(author=request.user).order_by('-created_date')

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the client object
            client = form.save()
            # Redirect to the client detail page
            return redirect('invoicer:read_client', client.slug)
    else:
        form = ClientForm()

    context = {
        'clients': clients,
        'form': form,
    }
    return render(request, 'invoicer/client/clients_list.html', context)


@login_required
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the client object
            client = form.save()
            # Redirect to the client detail page
            return redirect('invoicer:read_client', client.slug)
    else:
        form = ClientForm()

        context = {
            'form': form,
        }
        return render(request, 'invoicer/client/create_client.html', context)


@login_required
def read_client(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)

    context = {
        'client': client,
    }

    return render(request, 'invoicer/client/read_client.html', context)


@login_required
def delete_client(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)
    client.delete()

    return redirect('invoicer:clients_list')


@login_required
def update_client(request, client_slug):
    client = get_object_or_404(Client, slug=client_slug)

    form = ClientForm(
        request.POST or None,
        request.FILES or None,
        instance=client
    )

    if request.method == 'POST':
        if form.is_valid():

            # Delete the client logo if the delete_logo checkbox is checked
            if 'delete_logo' in request.POST:
                client.logo.delete(save=True)
                client.logo = None

            # Save the client object
            form.save()
            # Redirect to the client detail page
            return redirect('invoicer:read_client', client_slug=client_slug)

    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'invoicer/client/update_client.html', context)


@login_required
def invoices_list(request):
    invoices = Invoice.objects.filter(author=request.user).order_by('-created_date')

    context = {
        'invoices': invoices,
    }
    return render(request, 'invoicer/invoice/invoices_list.html', context)


@login_required
@transaction.atomic
def create_invoice(request):
    ServiceFormSet = formset_factory(ServiceForm)

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, user=request.user)
        service_formset = ServiceFormSet(request.POST)
        if invoice_form.is_valid() and service_formset.is_valid():
            # Save the invoice form
            invoice = invoice_form.save(commit=False)
            invoice.author = request.user
            invoice.save()

            # Save the service formset
            for service_form in service_formset:
                if service_form.is_valid():
                    service = service_form.save(commit=False)
                    service.invoice = invoice
                    service.author = request.user
                    service.save()

            return redirect('invoicer:invoices_list')

    elif request.method == 'GET':
        invoice_form = InvoiceForm(user=request.user)
        service_formset = ServiceFormSet()

    context = {
        'invoice_form': invoice_form,
        'service_formset': service_formset,
    }
    return render(request, 'invoicer/invoice/create_invoice.html', context)


@login_required
def read_invoice(request, invoice_slug):
    invoice = get_object_or_404(Invoice, slug=invoice_slug)

    context = {
        'invoice': invoice,
    }

    return render(request, 'invoicer/invoice/read_invoice.html', context)


@login_required
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()

    return redirect('invoicer:invoices_list')


@login_required
@transaction.atomic
def update_invoice(request, invoice_slug):
    invoice = get_object_or_404(Invoice, slug=invoice_slug, author=request.user)

    invoice_form = InvoiceForm(
        request.POST or None,
        request.FILES or None,
        instance=invoice,
        user=request.user
    )

    services = invoice.services.all()

    ServiceFormSet = formset_factory(ServiceForm, extra=0)
    initial_data = [{'id': service.id} for service in services]
    service_formset = ServiceFormSet(request.POST or None, initial=initial_data)

    if request.method == 'POST':
        if invoice_form.is_valid() and service_formset.is_valid():

            invoice_form.save()

            # Delete the old services of the invoice
            services.delete()

            # Create new services with the data from the formset
            new_services = []
            for form in service_formset:
                if form.cleaned_data:
                    service = form.save(commit=False)
                    service.invoice = invoice
                    new_services.append(service)

            # Save the new services
            Service.objects.bulk_create(new_services)

            return redirect('invoicer:read_invoice', invoice_slug=invoice_slug)

    context = {
        'invoice_form': invoice_form,
        'invoice': invoice,
        'services': services,
        'service_formset': service_formset,
    }

    return render(request, 'invoicer/invoice/update_invoice.html', context)


@login_required
def read_profile(request):
    profile = Profile.objects.filter(author=request.user).first()

    context = {
        'profile': profile,
    }

    return render(request, 'invoicer/profile/view_profile.html', context)


@login_required
def update_profile(request):
    profile = Profile.objects.filter(author=request.user).first()
    print("Got profile instance: {}".format(profile))

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )
    print("Got Profile Form")

    if request.method == 'POST':
        print("Request is Post Request")
        if form.is_valid():
            print("Form is valid")
            # Delete the client logo if the delete_logo checkbox is checked
            if 'delete_logo' in request.POST:
                profile.logo.delete(save=True)
                profile.logo = None

            # Save the client object
            try:
                form.save()
                print("Form was saved successfully")
            except Exception as e:
                print("Couldn't save the form. Exception: {}".format(e))
            # Redirect to the client detail page
            return redirect('invoicer:read_profile')
        else:
            print("Form is not valid")

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'invoicer/profile/update_profile.html', context)


@login_required
def export_invoice(request, invoice_slug):
    profile = Profile.objects.filter(author=request.user).first()
    invoice = get_object_or_404(Invoice, slug=invoice_slug)
    context = {
        'profile': profile,
        'invoice': invoice,
    }
    return render(request, 'invoicer/invoice/invoice_template.html', context)
