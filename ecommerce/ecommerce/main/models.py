from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.template.defaultfilters import slugify

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="E-mail", unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=30, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=30, blank=True)
    middle_name = models.CharField(verbose_name="Отчество", max_length=30, blank=True)

    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(('active'), default=True, help_text=(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    ),
                                    )
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)

class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=15)
    slug = models.SlugField(blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return str(self.name)

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, related_name='sellers', on_delete=models.CASCADE)

    @property
    def ticket_qty(self):
        return Ticket.objects.filter(seller=self)


    def __str__(self):
        return str(f'{self.user.first_name} {self.user.last_name}')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

class Ticket(models.Model):
    name = models.CharField(verbose_name="Название", max_length=15)
    text = models.CharField(verbose_name="Текст", max_length=200)
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="tickets")
    seller = models.ForeignKey(Seller, verbose_name="Продавец", related_name="tickets", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField()
    tag = models.ManyToManyField(Tag, verbose_name="Тег", related_name='tickets')
    price = models.PositiveIntegerField(verbose_name="Цена", default=1)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = "Объявления"
        ordering = ('-date_modified',)

    def __str__(self):
        return str(self.name)
