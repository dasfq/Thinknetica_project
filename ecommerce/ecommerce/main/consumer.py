# Встроенные импорты.
import json

# Импорты сторонних библиотек.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

# Импорты Django.
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.db.models import QuerySet

# Локальные импорты.
from main import models

class LiveChatConsumer(AsyncWebsocketConsumer):
    """ Класс для релизации чата """

    async def connect(self):
        """
        Функция срабатывает сразу как загружается шаблон. Добавляем текущего отправителя в группу.
        :param room_name: Имя комнаты.
        :param room_group_name: Имя группы. Сообщение будет отправлено всем в группе.
        :return: None
        :rtype: None
        """

        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")

        self.room_name = f"{self.scope['user'].first_name}_{self.scope['user'].last_name}"
        self.room_group_name = f'Game_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        """
        Функция приёма сообщений. Получает данные из шаблона.
        :param text_data: Получается данные из функции WebSocket.send(), прописанной в шаблоне.
        :type text_data:
        :return:
        :rtype:
        """
        data = json.loads(text_data)
        msg = data['text']

        ticket = await self.get_ticket_by_name(msg)

        if ticket:
            if ticket.is_sold:
                data = {
                    'status': 'sold',
                    'text': 'Данный товар уже продан =('
                }
            data = {
                'status': 'found',
                'title': ticket.name,
                'text': ticket.text,
                'price': ticket.price
            }
        else:
            data = {
                'status': 'not_found',
                'text': 'Данный товар не найден =('
            }


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": 'chatmsg',
                'message': data
            }
        )

    async def chatmsg(self, event):
        """
        Когда потправляем сообщение группе, нужно указать type и создать для него такую функцию.
        :param event:
        :type event:
        :return:
        :rtype:
        """
        msg = event['message']

        await self.send(
            text_data=json.dumps({
                'message': msg,
            })
        )

    @database_sync_to_async
    def get_ticket_by_name(self, keyword):
        """Вспомагательная функция. Ищет объявление по заголовку."""

        return models.TicketItem.objects.filter(name__contains=f'{keyword}').prefetch_related().last()

    async def disconnect(self, message):
        """
        Покинуть комнату группы
        :param message:
        :type message:
        :return:
        :rtype:
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
