import allure
import pytest
from service_method import market_method
import time
import configparser



ClientMethod = market_method.ClientMethod
ServiceMethod = market_method.ServiceMethod
Generat = market_method.GenerateData

config = configparser.ConfigParser()
config.read("settings.ini", encoding='utf-8')
secret_bank = url_adminka = config['market']['secret_bank']
token_secret_bank = config['market']['token_secret_bank']

@allure.epic('Негативные тесты hold')
class TestNegativeHold:
    @allure.story('hold с  неверным  partner_mnemocode')
    def test_hold_with_not_correct_partner(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()
        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance, partner_mnemocode="00000010")
        assert str(message_hold.text) == '{"status":"error","error_description":"Partner mnemocode is invalid"}', \
            message_hold.text

        user_balance_after = Client.get_balance(access_token_user=access_token_user)
        assert user_balance_after == user_balance, 'Произошло изменение баланса'

    @allure.story('hold с неверным bank_mnemocode')
    def test_hold_with_not_correct_bank_mnemocode(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()

        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance, bank_mnemocode="00000037")
        assert str(message_hold.text) == '{"status":"error","error_description":"Bank mnemocode is invalid"}', \
            message_hold.text

        user_balance_after = Client.get_balance(access_token_user=access_token_user)
        assert user_balance_after == user_balance, 'Произошло изменение баланса'

    @allure.story('hold с неверным user_id')
    def test_hold_with_not_correct_user_id(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()

        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance, user_id='12312')
        assert str(message_hold.text) == '{"status":"error","error_description":"User ID is invalid"}', \
            message_hold.text

        user_balance_after = Client.get_balance(access_token_user=access_token_user)
        assert user_balance_after == user_balance, 'Произошло изменение баланса'

    @allure.story('Холд с amount больше баланса')
    def test_hold_with_amount_more_balance(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()

        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance + 1)
        assert str(message_hold.text) == '{"status":"error","error_description":"Insufficient funds"}', \
            message_hold.text

        user_balance_after = Client.get_balance(access_token_user=access_token_user)
        assert user_balance_after == user_balance, 'Произошло изменение баланса'


@allure.epic('Негативные тесты unhold')
class TestNegativeUnhold():
    @allure.story('unhold с  неверным  partner_mnemocode')
    def test_unhold_with_not_correct_partner(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()

        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance)
        assert str(message_hold) == '<Response [200]>', message_hold

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_user, partner_mnemocode='1231212')
        assert str(code_unhold.text) == '{"status":"error","error_description":"Partner mnemocode is invalid"}',\
                                        str(code_unhold.text)

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_user)
        assert str(code_unhold) == '<Response [200]>', \
            str(code_unhold.text)

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == user_balance, f'Баланс {user_balance_new} '

    @allure.story('unhold с  неверным  bank_mnemocode')
    def test_unhold_with_not_correct_bank(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()

        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance)
        assert str(message_hold) == '<Response [200]>', message_hold

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_user,
            bank_mnemocode='1231212')
        assert str(code_unhold.text) == '{"status":"error","error_description":"Bank mnemocode is invalid"}', \
            str(code_unhold.text)

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_user)
        assert str(code_unhold) == '<Response [200]>', \
            str(code_unhold.text)

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == user_balance, f'Баланс {user_balance_new} '

    @allure.story('unhold с несуществующим transaction_id')
    def test_unhold_with_not_exist_transaction_id(self):
        generate = Generat()

        transaction_id = generate.get_transaction_id()
        refund_id = generate.get_refund_id()

        Service = ServiceMethod()
        access_token_service = Service.full_auth_service()

        Client = ClientMethod()
        access_token_user = Client.full_auth_client()

        user_balance = Client.get_balance(access_token_user=access_token_user)
        if user_balance < 2:
            Service.reward(transaction_id=int(transaction_id) - 1, access_token_service=access_token_service,
                           amount=62500)
            user_balance = Client.get_balance(access_token_user=access_token_user)

        message_hold = Client.hold(transaction_id=transaction_id, access_token_user=access_token_user,
                                   amount=user_balance)
        assert str(message_hold) == '<Response [200]>', message_hold

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=int(transaction_id)+1, refund_id=refund_id, access_token_service=access_token_user)
        assert str(code_unhold.text) == '{"status":"error","error_description":"Parent transaction not found"}', \
            str(code_unhold.text)

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_user)
        assert str(code_unhold) == '<Response [200]>', \
            str(code_unhold.text)

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == user_balance, f'Баланс {user_balance_new} '
