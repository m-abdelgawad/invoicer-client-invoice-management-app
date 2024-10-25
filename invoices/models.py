import random
import string
from django.db import models
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from crum import get_current_user
import itertools


# Create your models here.
class Client(models.Model):

    # Basic Fields
    first_name = models.CharField(null=True, blank=True, max_length=200)
    last_name = models.CharField(null=True, blank=True, max_length=200)
    company = models.CharField(null=True, blank=True, max_length=200)
    email_address = models.CharField(null=True, blank=True, max_length=100)
    mobile_number = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    logo = models.ImageField(null=True, blank=True, upload_to='invoicer_companies_logos/')
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, max_length=500, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoicer_clients',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('invoicer:read_client', args=[self.slug])

    def save(self, *args, **kwargs):
        user = get_current_user()
        self.author = user
        if self.created_date is None:
            self.created_date = timezone.localtime(timezone.now())

        if not self.id:
            # Check if the object has already been saved to the database.
            # If not, generate a slug for it.

            # Create a base slug string using the object's first and last name,
            # or email address and city/country if first and last name are not provided.
            if self.first_name and self.last_name:
                slug_str = f"{self.first_name}-{self.last_name}"
            else:
                slug_str = f"{self.email_address or self.mobile_number}-{self.city or self.country}"

            # Slugify the base slug string and save it as the object's slug field.
            self.slug = orig = slugify(slug_str)

            # If there is already another object with the same slug in the database,
            # append a counter to the end of the slug until it becomes unique.
            for x in itertools.count(1):
                if not Client.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f"{orig}-{x}"

        self.updated_date = timezone.localtime(timezone.now())

        super(Client, self).save(*args, **kwargs)


class Service(models.Model):

    CURRENCIES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('SAR', 'SAR'),
        ('EGP', 'EGP'),
    ]

    QUANTITY_UNITS = [
        ('Item', 'Item'),
        ('Hour', 'Hour'),
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month'),
    ]

    # Basic Fields
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    quantity_unit = models.CharField(choices=QUANTITY_UNITS, default='HOUR', max_length=100)
    unit_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    invoice = models.ForeignKey(
        'Invoice',
        on_delete=models.CASCADE,
        related_name='services',
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, max_length=500, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoicer_services',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        return '{}: {} {}'.format(self.title, self.total_price, self.currency)

    def save(self, *args, **kwargs):

        user = get_current_user()
        self.author = user

        if not self.id:

            self.created_date = timezone.localtime(timezone.now())

            # Generate the slug based on the title and timestamp
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S%f")
            base_slug = slugify(self.title)[:3]
            slug = f"{base_slug}-{timestamp}"

            # Ensure the slug is unique
            i = 1
            while Service.objects.filter(slug=slug).exists():
                slug = slugify(self.title)[:3] + '-' + str(timezone.now().strftime("%Y%m%d%H%M%S%f")) + '-' + str(i)
                i += 1
            self.slug = slug

        self.updated_date = timezone.localtime(timezone.now())

        super(Service, self).save(*args, **kwargs)


class Invoice(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
        ('Paid', 'Paid'),
    ]

    CURRENCIES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('SAR', 'SAR'),
        ('EGP', 'EGP'),
    ]

    title = models.CharField(null=True, blank=True, max_length=100)
    invoice_number = models.CharField(null=True, blank=True, max_length=100)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default='Pending', max_length=100)
    discount = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCIES, default='USD', max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, max_length=500, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoicer_invoices',
        blank=True,
        null=True,
        editable=False,
    )
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='invoices',
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{} {}'.format(self.title, self.invoice_number)

    def get_absolute_url(self):
        return reverse('invoicer:read_invoice', args=[self.slug])

    def get_total_price(self):
        total_price = 0
        for service in self.services.all():
            total_price += service.total_price
        return total_price

    def save(self, *args, **kwargs):

        user = get_current_user()
        self.author = user

        if not self.id:
            # Check if the object has already been saved to the database.
            # If not, generate the following:

            # The created date
            self.created_date = timezone.localtime(timezone.now())

            # The invoice number
            # get initials from client's company, first_name or last_name
            if self.client.company:
                initials = self.client.company[:3].upper()
            elif self.client.first_name:
                initials = self.client.first_name[:3].upper()
            elif self.client.last_name:
                initials = self.client.last_name[:3].upper()
            else:
                initials = ''.join(random.choices(string.ascii_uppercase, k=3))

            # find the latest invoice number for the client and increment by 1
            latest_invoice_number = Invoice.objects.filter(
                client=self.client,
                author=self.author
            ).aggregate(Max('invoice_number'))['invoice_number__max']
            if latest_invoice_number:
                sequence_number = int(latest_invoice_number[-5:]) + 1
            else:
                sequence_number = 1

            # format the invoice number and save the object
            self.invoice_number = '{}-{:05d}'.format(initials, sequence_number)

            # The slug
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S%f")
            slug = f"{self.invoice_number}-{timestamp}"

            # check if the slug is unique, and generate a new slug if not
            while Invoice.objects.filter(slug=slug).exists():
                sequence_number += 1
                slug = '{}-{:05d}'.format(initials, sequence_number)

            self.slug = slug

        self.updated_date = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)


class Profile(models.Model):

    first_name = models.CharField(null=True, blank=True, max_length=200)
    last_name = models.CharField(null=True, blank=True, max_length=200)
    company = models.CharField(null=True, blank=True, max_length=200)
    email_address = models.CharField(null=True, blank=True, max_length=100)
    mobile_number = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    logo = models.ImageField(null=True, blank=True, upload_to='users_profile_logos/')
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        self.author = user
        if self.created_date is None:
            self.created_date = timezone.localtime(timezone.now())
        self.updated_date = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)
