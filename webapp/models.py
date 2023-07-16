import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Property(models.Model):

    PROPERTY_TYPES = [
        ("Flat", "Flat"),
        ("House", "House"),
        ("Flatmate", "Flatmate"),
        ("Shop", "Shop"),
        ("Office", "Office"),
    ]
    BHK_TYPES = [
        ("1 RK", "RK"),
        ("1 BHK", "1 BHK"),
        ("2 BHK", "2 BHK"),
        ("2.5 BHK", "2.5 BHK"),
        ("3 BHK", "3 BHK"),
    ]

    CITY_LIST = [
        ("Pune", "Pune")
    ]

    LIST_TYPE = [
        ("Rent", "Rent"),
        ("Sale", "Sale")
    ]

    id = models.AutoField(primary_key=True, unique=True, auto_created=True)

    # image = models.ImageField(upload_to='images/', verbose_name="Property image")

    name = models.CharField(max_length=200, blank=False, help_text="Enter building / society name")
    area = models.CharField(max_length=200, blank=False, help_text="Ex : Wakad, Hinjewadi...") # area
    city = models.CharField(
        max_length=15,
        choices=CITY_LIST,
        default=CITY_LIST[0][0],
    )
    property_type = models.CharField(
        max_length=15,
        choices=PROPERTY_TYPES,
        default=PROPERTY_TYPES[0][0],
    )
    bhk_type = models.CharField(
        max_length=15,
        choices=BHK_TYPES,
        default=BHK_TYPES[1][0],
    )
    list_type = models.CharField(
        max_length=15,
        choices=LIST_TYPE,
        default=LIST_TYPE[0][0],
    )
    description = models.TextField(max_length=10000, blank=False, help_text="Enter detailed description like amenities, preferences, etc")
    rent = models.PositiveBigIntegerField(blank=False)
    deposit = models.PositiveBigIntegerField(blank=False)
    available_from = models.DateField(default=dt.date.today)
    owner_name = models.CharField(max_length=200, blank=False)
    ph_contact = models.CharField(max_length=12, blank=False)

    publisher = models.ForeignKey(User, related_name='publisher', on_delete=models.CASCADE, editable=False, blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    approver = models.ForeignKey(User, related_name='approver', on_delete=models.SET(get_sentinel_user), blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)

    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

