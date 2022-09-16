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



@allure.epic('Позитивные кейсы api')
class TestApiMarketPositive:
    @allure.story('Холд всей суммы -> анхолд под токеном пользователя')
    def test_hold_unhold_full_sum(self):
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
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_user)
        assert str(code_unhold) == '<Response [200]>', f'response_code {code_unhold}'

        user_balance_after_unhold = Client.get_balance(access_token_user=access_token_user)
        assert user_balance == user_balance_after_unhold, f' Баланс не равен первоначальному,  = {user_balance_after_unhold}'

    @allure.story('Холд вся сумма -1 -> анхолд')
    def test_hold_unhold_minus_1(self):
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
                                   amount=user_balance - 1)
        assert str(message_hold) == '<Response [200]>', message_hold

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 1, f'Баланс {user_balance_new} Ожидаю 0'

        code_unhold = Service.unhold(
            transaction_id=transaction_id, refund_id=refund_id, access_token_service=access_token_service)
        assert str(code_unhold) == '<Response [200]>', f'response_code {code_unhold}'

        user_balance_after_unhold = Client.get_balance(access_token_user=access_token_user)
        assert user_balance == user_balance_after_unhold, f' Баланс не равен первоначальному, = {user_balance_after_unhold}'

    @allure.story('Холд всей суммы -> clear -> reward')
    def test_hold_clear_reward_full_sum(self):
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

        code_clear = Service.clear(transaction_id=transaction_id, access_token_service=access_token_service)
        assert str(code_clear) == '<Response [200]>', f'response_code {code_clear}'

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_reward = Service.reward(
            transaction_id=int(transaction_id) + 1, access_token_service=access_token_service, amount=user_balance)
        assert str(code_reward) == '<Response [200]>', f'response_code {code_reward}'

        user_balance_after_reward = Client.get_balance(access_token_user=access_token_user)
        assert user_balance == user_balance_after_reward, f' Баланс не равен первоначальному,  = {user_balance_after_reward}'

    @allure.story('Холд всей суммы -1 -> clear -> reward')
    def test_hold_clear_reward_minus_1(self):
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
                                   amount=user_balance - 1)
        assert str(message_hold) == '<Response [200]>', message_hold

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 1, f'Баланс {user_balance_new} Ожидаю 1'

        code_clear = Service.clear(transaction_id=transaction_id, access_token_service=access_token_service)
        assert str(code_clear) == '<Response [200]>', f'response_code {code_clear}'

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 1, f'Баланс {user_balance_new} Ожидаю 1'

        code_reward = Service.reward(
            transaction_id=int(transaction_id) + 1, access_token_service=access_token_service, amount=user_balance - 1)
        assert str(code_reward) == '<Response [200]>', f'response_code {code_reward}'

        user_balance_after_reward = Client.get_balance(access_token_user=access_token_user)
        assert user_balance == user_balance_after_reward, f' Баланс не равен первоначальному,  = {user_balance_after_reward}'

    @allure.story('Холд всей суммы  -> clear -> refund за 1 раз')
    def test_hold_clear_refund_full_sum(self):
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

        code_clear = Service.clear(transaction_id=transaction_id, access_token_service=access_token_service)
        assert str(code_clear) == '<Response [200]>', f'response_code {code_clear}'

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_refund = Service.refund(transaction_id=transaction_id, access_token_service=access_token_service,
                                     amount=user_balance, refund_id=refund_id)
        assert str(code_refund) == '<Response [200]>', code_refund

        user_balance_after_refund = Client.get_balance(access_token_user=access_token_user)
        assert user_balance == user_balance_after_refund, f' Баланс не равен первоначальному,  = {user_balance_after_refund}'

    @allure.story('Холд всей суммы  -> clear -> refund за 2 раз')
    def test_hold_clear_refund_part_sum(self):
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

        code_clear = Service.clear(transaction_id=transaction_id, access_token_service=access_token_service)
        assert str(code_clear) == '<Response [200]>', f'response_code {code_clear}'

        user_balance_new = Client.get_balance(access_token_user=access_token_user)
        assert int(user_balance_new) == 0, f'Баланс {user_balance_new} Ожидаю 0'

        code_refund = Service.refund(transaction_id=int(transaction_id), access_token_service=access_token_service,
                                     amount=user_balance - 2, refund_id=int(refund_id) + 2)
        assert str(code_refund) == '<Response [200]>', code_refund

        user_balance_after_refund = Client.get_balance(access_token_user=access_token_user)
        assert user_balance - 2 == user_balance_after_refund, f' Баланс не равен первоначальному,  = {user_balance_after_refund}'

        code_refund = Service.refund(transaction_id=int(transaction_id), access_token_service=access_token_service,
                                     amount=2, refund_id=int(refund_id) + 1)
        assert str(code_refund) == '<Response [200]>', code_refund

        user_balance_after_refund = Client.get_balance(access_token_user=access_token_user)
        assert user_balance == user_balance_after_refund, f' Баланс не равен первоначальному,  = {user_balance_after_refund}'

