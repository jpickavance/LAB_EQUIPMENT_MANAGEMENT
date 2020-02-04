from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_staff=False, is_admin=False, is_active=False):
        if not email:
            raise ValueError("Users must have a valid email address")
        if not password:
            raise ValueError("Users must have a password")
        else:
            user_obj = self.model(
                email = self.normalize_email(email)
            )
            user_obj.set_password(password) # set/change user password
            user_obj.full_name = full_name
            user_obj.staff = is_staff
            user_obj.admin = is_admin
            user_obj.active = is_active
            user_obj.save(using=self._db)
            return user_obj
    
    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            password = password,
            is_active = True,
            is_staff = True
        )
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            password = password,
            is_active = True,
            is_staff =  True,
            is_admin = True,
        )
        return user

class User(AbstractBaseUser):
    email          = models.EmailField(unique=True, max_length=255)
    full_name      = models.CharField(max_length=255, blank=True, null=True)
    active         = models.BooleanField(default=True) #can login
    staff          = models.BooleanField(default=False) #staff non-superuser
    admin          = models.BooleanField(default=False)
    confirm_email  = models.BooleanField(default=False) 
    image          = models.ImageField(default='default.jpg', upload_to='profile_pics')
    timestamp      = models.DateTimeField(auto_now_add=True)
    slug           = models.SlugField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    #email and password are required by default
    REQUIRED_FIELDS = [
        'full_name'
    ]

    objects = UserManager()

    def __str__(self): 
        return self.email
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name + ' ' + self.email)
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("accounts:profile-detail", kwargs={"slug":self.slug})
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active
