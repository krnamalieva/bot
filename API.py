import logging
from datetime import datetime
from typing import Dict
from time import sleep
from geo import Ip, Point
from geo.abstract import HttpService
from telegram.classes import Webhook, Chat, User, Message


class TelegramApi:
    url: str = 'https://core.telegram.org/bots/api'

    def __init__(self, token: str, http: HttpService):
        self.__token = 6108877297:AAHKG8eDRceSh1pLuMfFpLzpLEvzh_YCzy0
        self.__http = http

    def auth(self):
        response = self.__http.get(f'{self.url}/bot{self.__token}/getMe')
        if not response or not response.get('ok'):
            raise Exception(f'Can not connect to telegram ({response.status})')

    @property
    def webhook(self) -> Webhook | None:
        sleep(1)
        try:
            response = self.__http.get(
                url=f'{self.url}/bot{self.__token}/getWebhookInfo'
            )
            if not response:
                return
            result = response.get('result')
            url = result.get('url')
            ip_address = result.get('ip_address')
            if not url or not ip_address:
                raise Exception(result)
            return Webhook(url=url, ip=Ip(ip_address))
        except Exception as e:
            logging.error(e)

    @webhook.setter
    def webhook(self, url: str):
        try:
            response = self.__http.get(
                url=f'{self.url}/bot{self.__token}/setWebhook',
                headers={'Content-Type': 'application/json'},
                params={
                    'url': url,
                }
            )
            description = response.get('description', response)
            logging.info(description)
            if not response.get('result', False):
                raise Exception(description)
        except Exception as e:
            logging.error(e)

    @webhook.deleter
    def webhook(self):
        try:
            response = self.__http.post(
                url=f'{self.url}/bot{self.__token}/deleteWebhook',
                headers={'Content-Type': 'application/json'}
            )
            description = response.get('description')
            logging.info(description)
            if not response.get('result', False):
                raise Exception(description)
        except Exception as e:
            logging.error(e)

    @staticmethod
    def parse(data: Dict) -> Message:
        message = data.get('message', data)
        text = message.get('text', '')
        date = message.get('date', None)
        user = message.get('from', dict())
        chat = message.get('chat', dict())
        location = message.get('location', None)
        if date:
            date = datetime.fromtimestamp(int(date))
        if location:
            location = Point(
                lat=location.get('latitude'),
                lng=location.get('longitude'),
            )
        return Message(
            text=text,
            chat=Chat(id=chat.get('id')),
            user=User(
                id=user.get('id'),
                firstname=user.get('first_name'),
                lastname=user.get('last_name'),
                is_bot=user.get('is_bot', False)
            ),
            date=date,
            id=message.get('message_id', 0),
            location=location
        )

    def send_message(self, message: Message) -> Message | None:
        sleep(1)
        try:
            response = self.__http.get(
                url=f'{self.url}/bot{self.__token}/sendMessage',
                params={
                    'chat_id': message.chat.id,
                    'text': message.text
                }
            )
            if not response or not response.get('ok'):
                return
            return self.parse(response.get('result', dict()))
        except Exception as e:
            logging.error(e)

    def send_location(self, chat: Chat, point: Point):
        sleep(1)
        try:
            response = self.__http.get(
                url=f'{self.url}/bot{self.__token}/sendLocation',
                params={
                    'chat_id': chat.id,
                    'latitude': point.lat,
                    'longitude': point.lng
                }
            )
            if not response or not response.get('ok'):
                return
            return self.parse(response.get('result', dict()))
        except Exception as e:
            logging.error(e)

    @staticmethod
    def connect(token: str, webhook_url: str, http: HttpService):
        telegram = TelegramApi(token, http)
        telegram.auth()
        telegram.webhook = webhook_url
        return telegram
