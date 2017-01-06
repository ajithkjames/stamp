from django.db import models
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime, timedelta

SIZE_CHOICES = (
        (0, 'small'),
        (1, 'medium'),
        (2, 'large')
)


class ModelManager(models.Manager):
        def get_queryset(self, fetch_all=False):
                return super(ModelManager, self).get_queryset() if fetch_all \
                        else super(ModelManager, self).get_queryset().filter(deleted_at__isnull=True)


class DateMixin(models.Model):

        objects = ModelManager()

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        deleted_at = models.DateTimeField(null=True, blank=True)

        class Meta:
                abstract = True

class Profile(DateMixin):

    user = models.OneToOneField(User)
    company = models.CharField(max_length=1000, null=True, blank=True)
    designation = models.CharField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):              # __unicode__ on Python 2
            return self.user.username


class OrderDetail(DateMixin):

    user = models.OneToOneField(User)
    stamp_type = models.CharField(max_length=1000, null=True, blank=True)
    size = models.IntegerField(choices=SIZE_CHOICES, null=True, blank=True)
    font = models.CharField(max_length=1000, null=True, blank=True)
    color = models.CharField(max_length=1000, null=True, blank=True)
    allignment = models.CharField(max_length=1000, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    request = models.CharField(max_length=1000, null=True, blank=True)
    advance = models.IntegerField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
            return self.stamp_type
