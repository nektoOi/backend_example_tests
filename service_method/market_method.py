import allure
import requests
import time
import jwt
import configparser
from datetime import datetime
from random import randrange

config = configparser.ConfigParser()
config.read("settings.ini", encoding='utf-8')

url_adminka = config['market']['url_adminka']
pass_adminka = config['market']['pass_adminka']
login_adminka = config['market']['login_adminka']
url_bank = config['market']['url_bank']
externalId_client = config['market']['externalId_client']
end_point = config['market']['end_point']
profile_id = config['market']['profile_id']
secret_market = config['market']['secret_market']
token_secret_market = config['market']['token_secret_market']
secret_client = config['market']['secret_client']


class GenerateData:

    def __init__(self):
        self.refund_id = None
        self.transaction_id = None
        self.current_datetime = datetime.now()

    def get_transaction_id(self):
        """Генерирует уникальный transaction_id"""

        self.transaction_id = (str(self.current_datetime.strftime("%Y%m%d%H%M%S"))) + str(randrange(1, 999))
        return self.transaction_id

    def get_refund_id(self):
        """Генерирует уникальный transaction_id"""

        self.refund_id = (str(self.current_datetime.strftime("%Y%m%d%H%M%S"))) + str(randrange(1, 999))
        return self.refund_id


class ClientMethod:

    def auth_adminka(self):
        """Авторизуется в админке Получает access_token """

        with allure.step('Авторизуется в админке Получает access_token'):
            sess = requests.Session()
            url = f'https://{url_adminka}/api/auth/login'
            payload = {"email": login_adminka,
                       "password": pass_adminka
                       }

            request = sess.post(url=url, data=payload)
            access_token = request.json()['data']['access_token']
            return access_token

    def get_url_to_lk(self, access_token=auth_adminka):
        """Генерирует ссылку для входа в ЛК"""

        with allure.step('Генерирует ссылку для входа в ЛК'):
            headers = {'authorization': f'Bearer {access_token}'}
            request1 = requests.post(
                url=f'https://{url_adminka}/api/auth/asadmin?externalId={externalId_client}&domain={url_bank}',
                headers=headers)
            link_to_lk_under_client = request1.json()['data']['authorizationLink']
            return link_to_lk_under_client

    def get_session_token(self, url=get_url_to_lk):
        """Получает session_token при авторизации в ЛК"""

        with allure.step('Получает session_token при авторизации в ЛК'):
            secret = url.split('secret=')[1]
            r = requests.get(
                f'https://{url_bank}/00000001/v2/auth/stage/token?client_id={externalId_client}&secret={secret}')
            session_token = r.json()['session_token']

        return session_token

    def get_user_token(self, session_token=get_session_token):
        """Получает user_token через метод авторизации"""

        with allure.step('Получает user_token через метод авторизации'):
            request = requests.get(f'https://{end_point}/auth/user-token?token={session_token}')
            try:
                user_token = request.json()['user_token']
            except:
                user_token = request

            return user_token

    def redirect(self, user_token=get_user_token):
        """Получает redirect_token через метод авторизации"""

        with allure.step('Получает redirect_token через метод авторизации'):
            requests.Session()
            url = f'https://{end_point}/auth/authorize?partnerId=73&redirectUrl=https://www.rambler.ru&userToken={user_token}'
            request = requests.get(url)
            print(url)
            print(request.url)
            redirect_token = request.url.split('code=')[1]
            time.sleep(0.1)
            return redirect_token

    def get_access_token_user(self, auth_code: str = redirect, partner_id=73, secret_client=secret_client):
        """Получает access_token_user через метод авторизации"""

        with allure.step('Получает access_token_user через метод авторизации'):
            url = f'https://{end_point}/auth/token'
            payload = {
                "auth_code": auth_code,
                "partner_id": partner_id,
                "secret": secret_client
            }
            request = requests.post(url=url, json=payload)
            try:
                access_token_user = request.json()['access_token']
                print('access_token_user --- ' + access_token_user)
            except:
                access_token_user = request
            return access_token_user

    def full_auth_client(self):
        """Получение клиентского token для работы с методами этикетки"""

        with allure.step('Получение клиентского token для работы с методами этикетки'):
            auth_adminka = self.auth_adminka()
            url_to_lk = self.get_url_to_lk(access_token=auth_adminka)
            session_token = self.get_session_token(url=url_to_lk)
            user_token = self.get_user_token(session_token=session_token)
            code_auth = self.redirect(user_token=user_token)
            token = self.get_access_token_user(auth_code=code_auth)
            return token

    def get_balance(self, access_token_user=get_access_token_user):
        """Получает баланс клиента"""

        with allure.step(f'Получает баланс клиента '):
            headers = {'authorization': f'Bearer {access_token_user}'}
            request = requests.get(
                f'https://{end_point}/api/partner/bonus/v1/balances?bank_mnemocode=00000010&'
                f'user_id={profile_id}&partner_mnemocode=00000037',
                headers=headers)
            print(request)
            print(request.json())
            balance = request.json()['balances'][0]['amount']
            with allure.step(f'Баланс клиента = {balance}'):
                print('balance ---' + str(balance))
                return balance

    def hold(self, transaction_id, access_token_user=get_access_token_user, amount: int = get_balance,
             partner_mnemocode="00000037", bank_mnemocode="00000010", user_id=profile_id):
        """Холдирует баллы клиента"""

        with allure.step(f'hold - Холдирует {amount} баллы клиента '
                         f'под bank_mnemocode - {bank_mnemocode}  partner_mnemocode - {partner_mnemocode}'):
            print(amount)
            headers = {'authorization': f'Bearer {access_token_user}'}
            payload = {
                "partner_mnemocode": partner_mnemocode,
                "bank_mnemocode": bank_mnemocode,
                "user_id": user_id,
                "money_movement": {
                    "amount": amount,
                    "currency": "RUB"
                },
                "bonus_movement": [
                    {
                        "amount": amount,
                        "currency": "AWL"
                    }
                ],

                "order_id": "21231251",
                "transaction_id": transaction_id,
                "merchant_name": "test_merch",
                "transaction_date": "2022-03-30",
                "mcc": "5412",
                "category": "test_cat"
            }
            request = requests.post(url=f'https://{end_point}/api/partner/bonus/v1/hold', json=payload, headers=headers)

            print(request)
            with allure.step(f'Получаем ответ {request.text}'):
                return request


class ServiceMethod:

    def get_service_jwt(self, partner_mnemocode="00000037", bank_mnemocode="00000010", secret_market=secret_market):
        """Генерирует jwt токен для сервисной авторизации """

        with allure.step('Генерирует jwt токен для сервисной авторизации'):
            encoded_jwt = jwt.encode({"partner_mnemocode": partner_mnemocode,
                                      "bank_mnemocode": bank_mnemocode,
                                      "secret": secret_market},
                                     token_secret_market, algorithm="HS256")

            print(encoded_jwt)
            return encoded_jwt

    def get_service_access_token(self, encoded_jwt):
        """Получает service_access_token"""

        with allure.step('Получает service_access_token'):
            payload = {
                "token": encoded_jwt
            }
            request = requests.post(f'https://{end_point}/auth/service/token',
                                    json=payload)
            try:
                access_token = request.json()['access_token']
                print('service_access_token --- ' + access_token)
            except:
                access_token = request.json()
            return access_token

    def full_auth_service(self):
        service_jwt = self.get_service_jwt()
        service_access_token = self.get_service_access_token(encoded_jwt=service_jwt)
        return service_access_token

    def unhold(self, transaction_id, refund_id, access_token_service, partner_mnemocode="00000037",
               bank_mnemocode="00000010"):
        """unhold - возвращает захолдированные баллы """

        with allure.step(f'unhold - возвращает захолдированные баллы по транзакции {transaction_id} '
                         f'под bank_mnemocode - {bank_mnemocode}  partner_mnemocode - {partner_mnemocode}'):
            headers = {'authorization': f'Bearer {access_token_service}'}
            payload = {
                "partner_mnemocode": partner_mnemocode,
                "bank_mnemocode": bank_mnemocode,
                "transaction_id": transaction_id,
                "refund_id": refund_id
            }
            request = requests.post(url=f'https://{end_point}/api/partner/bonus/v1/unhold', json=payload,
                                    headers=headers)
            with allure.step(f'Получаем ответ {request.text}'):
                return request

    def clear(self, transaction_id, access_token_service, partner_mnemocode="00000037", bank_mnemocode='00000010'):
        """clear - постирует захолдированные транзакции"""

        with allure.step(f'clear - постирует захолдированные транзакции {transaction_id} '
                         f'под bank_mnemocode - {bank_mnemocode}  partner_mnemocode - {partner_mnemocode}'):
            headers = {'authorization': f'Bearer {access_token_service}'}
            payload = {
                "partner_mnemocode": partner_mnemocode,
                "bank_mnemocode": bank_mnemocode,
                "transaction_id": transaction_id
            }
            request = requests.post(url=f'https://{end_point}/api/partner/bonus/v1/clear', json=payload,
                                    headers=headers)

            print(request.text)
            with allure.step(f'Получаем ответ {request.text}'):
                return request

    def reward(self, transaction_id, access_token_service, amount: int,
               partner_mnemocode="00000037", bank_mnemocode="00000010"):
        """reward - начисляет баллы клиенту"""

        with allure.step(f'reward - Начисляет {amount} баллов по транзакции {transaction_id} '
                         f'под bank_mnemocode - {bank_mnemocode}  partner_mnemocode - {partner_mnemocode}'):
            headers = {'authorization': f'Bearer {access_token_service}'}
            payload = {
                "partner_mnemocode": partner_mnemocode,
                "bank_mnemocode": bank_mnemocode,
                "transaction_id": str(transaction_id),
                "user_id": profile_id,
                "order_id": "1233212",
                "bonuses": [
                    {
                        "amount": amount,
                        "currency": "AWL"
                    }
                ],
                "reason": "231232"
            }
            request = requests.post(url=f'https://{end_point}/api/partner/bonus/v1/reward', json=payload,
                                    headers=headers)

            print(request.text)
            with allure.step(f'Получаем ответ {request.text}'):
                return request

    def refund(self, transaction_id, access_token_service, amount: int, refund_id,
               partner_mnemocode='00000037', bank_mnemocode='00000010', user_id=profile_id):
        """refund - возвращает запостированные баллы"""

        with allure.step(f'refund - Возвращает {amount} баллов по транзакции  {transaction_id} '
                         f'под bank_mnemocode - {bank_mnemocode}  partner_mnemocode - {partner_mnemocode}'):
            headers = {'authorization': f'Bearer {access_token_service}'}
            payload = {
                "partner_mnemocode": partner_mnemocode,
                "bank_mnemocode": bank_mnemocode,
                "transaction_id": transaction_id,
                "user_id": user_id,
                "refund_id": refund_id,
                "order_id": "1231232",
                "money_movement": {
                    "amount": amount,
                    "currency": "RUB"
                },
                "bonus_movement": [
                    {
                        "amount": amount,
                        "currency": "AWL"
                    }
                ]
            }
            request = requests.post(url=f'https://{end_point}/api/partner/bonus/v1/refund', json=payload,
                                    headers=headers)

            print(request.text)
            with allure.step(f'Получаем ответ {request.text}'):
                return request
