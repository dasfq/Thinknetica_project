from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from .managers import CustomUserManager
from django.template.defaultfilters import slugify
from django.urls import reverse


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model from :class:'django.contrib.auth.base_user.AbstractBaseUser' class.

    :param username: User's username
    :type username: str, optional
    :param email: User's email
    :type email: 'models.EmailField'
    :param first_name: First name
    :type first_name: str, optional
    :param group: permission groups which user is in
    :type group: str, optional
    """
    username = models.CharField(verbose_name="Логин", null=True, blank=True, max_length=10)
    email = models.EmailField(verbose_name="E-mail", unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=30, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=30, blank=True)
    middle_name = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
    group = models.ManyToManyField(Group, verbose_name="Группа", related_name='users', blank=True)

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

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Profile(CustomUser):
    """Класс для профиля пользователя. Нужно объединить его с CustomUser и оставить один.

    :param birth_date: Дата рождения
    :type birth_date: 'models.DateTimeField'
    :param avatar: Аватарка пользователя
    :type avatar: 'models.ImageField'
    """
    birth_date = models.DateTimeField(blank=True)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default_ava.png')
    phone_number = models.CharField(max_length=12, verbose_name="Номер телефона", null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_absolute_url(self) -> str:
        """Функция определения url к объекту :class:'Profile'

        :return: url к объекту :class:'Profile'
        :rtype: str, optional
        """
        return reverse('profile_update', kwargs={'pk': self.pk})


class Category(models.Model):
    """Класс категории объявления.

    :param slug: Короткое название категории (слаг). Автоматически генерируется.
    :type slug: 'models.SlugField'
    """

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

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        """Переопределение метода save() с добавлением генерации значения для поля :param slug.
        """

        if self.slug is None:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return str(f'{self.user.first_name} {self.user.last_name}')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class BaseTicket(models.Model):
    """Абстрактный класс объявления.
    """

    name = models.CharField(verbose_name="Название", max_length=25)
    text = models.CharField(verbose_name="Текст", max_length=200)
    seller = models.ForeignKey(Seller, verbose_name="Продавец", related_name="%(app_label)s_%(class)s_seller",
                               on_delete=models.CASCADE, related_query_name='%(app_label)s_%(class)s_seller')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, verbose_name="Тег", related_name='%(app_label)s_%(class)s_tag',
                                 related_query_name='%(app_label)s_%(class)s_tag')
    price = models.PositiveIntegerField(verbose_name="Цена", default=1)
    is_sold = models.BooleanField(verbose_name='Продано', default=False)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = "Объявления"
        ordering = ('-date_modified',)
        abstract = True

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return self.car.name + str(self.id)


class Subscriber(models.Model):
    profile = models.OneToOneField(Profile, verbose_name="Подписчик", on_delete=models.CASCADE, related_name="subscribers")
    is_active = models.BooleanField(verbose_name='Подписка активна', default=True)
    from_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self) -> str:
        return str(self.profile)


class SMSLog(models.Model):
    """Класс для хранения данных после отправки СМС через Twillio
    """

    code = models.CharField(max_length=4, verbose_name="Код")
    response = models.JSONField(max_length=50, verbose_name="Ответ сервера")
    phone_number = models.CharField(max_length=12, verbose_name="Номер телефона")
