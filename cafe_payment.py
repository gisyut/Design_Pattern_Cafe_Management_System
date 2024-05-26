from abc import ABC, abstractmethod
class Cafe_handler:
    def __init__(self):
        self.payments = {}

        self.cash_handler = CashHandler(self)
        self.credit_card_handler = CreditCardHandler(self)
        self.debit_card_handler = DebitCardHandler(self)
        self.gifticon_handler = GifticonHandler(self)

        self.cash_handler.set_next(self.credit_card_handler)
        self.credit_card_handler.set_next(self.debit_card_handler)
        self.debit_card_handler.set_next(self.gifticon_handler)

    def add_payment(self, method, amount):
        if method in self.payments:
            self.payments[method] += amount
        else:
            self.payments[method] = amount

    def handle_payment(self, req):
        self.cash_handler.handle(req)

class Handler:
    def __init__(self, cafe_handler=None):
        self.next_handler = None
        self.cafe_handler = cafe_handler

    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, req):
        if self.next_handler:
            return self.next_handler.handle(req)
        print("All handlers failed")
        return None

class CashHandler(Handler):
    def handle(self, req):
        if req["method"] == "cash":
            self.cafe_handler.add_payment(req["method"], req["amount"])
        else:
            super().handle(req)

class CreditCardHandler(Handler):
    def handle(self, req):
        if req["method"] == "creditCard":
            self.cafe_handler.add_payment(req["method"], req["amount"])
        else:
            super().handle(req)

class DebitCardHandler(Handler):
    def handle(self, req):
        if req["method"] == "debitCard":
            self.cafe_handler.add_payment(req["method"], req["amount"])
        else:
            super().handle(req)

class GifticonHandler(Handler):
    def handle(self, req):
        if req["method"] == "Gifticon":
            self.cafe_handler.add_payment(req["method"], req["amount"])
        else:
            super().handle(req)

class FinancialStatementSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.total_amount = 0
        return cls._instance

    def update(self, amount):
        self.total_amount += amount
        print(f"Updated financial statement: total amount is now {self.total_amount}")

# Observer 패턴: 결제 내역 관찰
class PaymentObserver(ABC):
    @abstractmethod
    def update(self, amount):
        pass

class FinancialStatementObserver(PaymentObserver):
    def __init__(self):
        self.financial_statement = FinancialStatementSingleton()

    def update(self, amount):
        self.financial_statement.update(amount)

class Payment:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, amount):
        for observer in self.observers:
            observer.update(amount)

    def make_payment(self, req, handler):
        handler.handle_payment(req)
        self.notify_observers(req["amount"])

# 시스템 동작 예제
if __name__ == "__main__":
    # 결제 팩토리 생성
    payment_handler = Cafe_handler()
    
    # 재무제표 관찰자 생성
    financial_observer = FinancialStatementObserver()
    
    # 결제 시스템 생성
    payment_system = Payment()
    payment_system.add_observer(financial_observer)

    req1 = {"method": "creditCard", "amount": 10000}
    req2 = {"method": "cash", "amount": 5000}
    req3 = {"method": "Gifticon", "amount": 2000}

    payment_system.make_payment(req1, payment_handler)
    payment_system.make_payment(req2, payment_handler)
    payment_system.make_payment(req3, payment_handler)

    print(payment_handler.payments)