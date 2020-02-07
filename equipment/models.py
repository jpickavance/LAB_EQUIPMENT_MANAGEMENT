from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.shortcuts import redirect
from accounts.models import User

# Create your models here.
class Item(models.Model):
    equipment       = models.CharField(max_length=120)
    brand           = models.CharField(max_length=36)
    model_spec      = models.CharField(max_length=36)
    category        = models.CharField(max_length=36, default='Item type')
    ICON_ref        = models.CharField(max_length=36)
    availability    = models.BooleanField(default=True)
    borrow_date     = models.DateField(null=True, blank=True)
    return_date     = models.DateField(null=True, blank=True)
    asset_number    = models.CharField(null=True, blank=True, max_length=32)
    serial_number   = models.CharField(null=True, blank=True, max_length=32)
    location        = models.CharField(null=True, blank=True, max_length=120, default="storeroom")
    value           = models.CharField(null=True, blank=True, max_length=10)
    PAT             = models.DateField(null=True, blank=True)
    current_user    = models.EmailField(null=True, blank=True, max_length=72, default='')
    comments        = models.TextField(null=True, blank=True)
    db_user         = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    slug            = models.SlugField(null=True, blank=True)

    #name object to "Equipment: equipment(x)"
    def __str__(self): 
        return 'Equipment: ' + self.equipment + '(' + self.ICON_ref + ')'

    #automatically save slug field on create
    def save(self, *args, **kwargs):
        self.slug = slugify(self.equipment + ' ' + self.ICON_ref)
        super(Item, self).save(*args, **kwargs)

    #function for model that allows url linking (use {{object.get_absolute_url}} in relevent template html)
    def get_absolute_url(self):
        return reverse("equipment:item-book", kwargs={"slug":self.slug}) #reverse lookup from urls.py, using name of path
        #f"{self.slug}"
    
    @property
    def get_myfield(self):
        if self.return_date == None:
              return "yes"
        else:
              return self.return_date
