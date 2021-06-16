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




class Profile(CustomUser):
    birth_date = models.DateTimeField(blank=True)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default_ava.png')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



class Category(models.Model):

    class CatChoices(models.TextChoices):
        ITEMS = 'items', 'Вещи'
        CARS = 'cars', 'Авто'
        SERVICES = 'services', 'услуги'

    name = models.CharField(verbose_name='Название категории', max_length=15)
    slug = models.SlugField(unique=True, default='')


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.slug is None:
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
        subclasses = BaseTicket.__subclasses__()
        count = 0
        for i in subclasses:
            count += i.objects.filter(seller=self).count()
        return count

    def __str__(self):
        return str(f'{self.user.first_name} {self.user.last_name}')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

class BaseTicket(models.Model):
    name = models.CharField(verbose_name="Название", max_length=25)
    text = models.CharField(verbose_name="Текст", max_length=200)
    seller = models.ForeignKey(Seller, verbose_name="Продавец", related_name="%(app_label)s_%(class)s_seller",
                               on_delete=models.CASCADE, related_query_name='%(app_label)s_%(class)s_seller')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, verbose_name="Тег", related_name='%(app_label)s_%(class)s_tag',
                                 related_query_name='%(app_label)s_%(class)s_tag')
    price = models.PositiveIntegerField(verbose_name="Цена", default=1)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = "Объявления"
        ordering = ('-date_modified',)
        abstract = True

    def __str__(self):
        return str(self.name)


class TicketService(BaseTicket):
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="TicketServices")
    term_days = models.PositiveIntegerField(verbose_name='Срок выполнения')
    warranty_days = models.PositiveIntegerField(verbose_name='Гарантийный срок')

    class Meta(BaseTicket.Meta):
        verbose_name = 'Объявление - услуги'
        verbose_name_plural = 'Объявления - услуги'

class TicketCar(BaseTicket):
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="TicketCars")
    model = models.CharField(verbose_name='Модель', max_length=10)
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    color = models.CharField(verbose_name='Цвет', max_length=10)

    class Meta(BaseTicket.Meta):
        verbose_name = 'Объявление - авто'
        verbose_name_plural = 'Объявления - авто'

class TicketItem(BaseTicket):
    STATE_CHOICES = [
        ('new', 'новое'),
        ('used', 'б/у')
    ]

    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="TicketItems")
    state = models.CharField(verbose_name="Состояние", max_length=10, choices=STATE_CHOICES)
    qty = models.PositiveIntegerField(verbose_name='Количество')

    class Meta(BaseTicket.Meta):
        verbose_name = 'Объявление - вещи'
        verbose_name_plural = 'Объявления - вещи'


class TicketServiceArchive(TicketService):

    class Meta:
        verbose_name_plural = 'Архив - Услуги'
        proxy = True


class TicketCarArchive(TicketCar):

    class Meta:
        verbose_name_plural = 'Архив - Авто '
        proxy = True


class TicketItemArchive(TicketItem):

    class Meta:
        verbose_name_plural = 'Архив - Вещи'
        proxy = True


class Picture(models.Model):
    car = models.ForeignKey(TicketCar, on_delete=models.CASCADE, verbose_name='Автомобили', related_name='pictures')
    image = models.ImageField(upload_to='', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.car.name+str(self.id)