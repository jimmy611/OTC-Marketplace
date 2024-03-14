from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

CRYPTO_CHOICES = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('LTC', 'Litecoin'),
    # Add more cryptocurrencies here
)

STATUS_CHOICES = (
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

BUY_SELL_CHOICES = (
    ('buy', 'Buy'),
    ('sell', 'Sell'),
)

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'marketplace'  # Add this line

    def __str__(self):
        return self.name

class Blockchain(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    crypto = models.CharField(max_length=3, choices=CRYPTO_CHOICES)
    buy_sell = models.CharField(max_length=4, choices=BUY_SELL_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')
    date = models.DateTimeField(auto_now_add=True)
    
    # add more fields if necessary
    def __str__(self):
        return f"{self.user.username}'s {self.type} transaction of {self.quantity} {self.symbol} at ${self.price}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')