from ..main.models import Ticket

tickets = Ticket.objects.all()
realty = tickets.filter(category__name='Недвижимость')
servives = tickets.filter(category__name='Работа')
cars = tickets.filter(category__name="Автомобили")

print(realty)