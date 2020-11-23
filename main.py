import random
from enum import Enum, auto


class Product(Enum):
    A = auto()
    B = auto()

    def __str__(self):
        return self.name


class EcoAgent:
    def __init__(self, name, product, good, produce_per_turn, money):
        self.name = name
        self.product = product
        self.good = good
        self.money = money
        self.produce_per_turn = produce_per_turn
        self.product_qty = 0
        self.good_qty = 0
        self.price_rate = 10

    def produce(self):
        self.product_qty += self.produce_per_turn

    def consume(self):
        self.good_qty = 0

    def get_demand(self):
        return Demand(self, self.good, self.money)

    def get_price(self, last_price=None):
        if last_price is None or last_price == 0:
            price = self.money // self.product_qty
        else:
            if self.product_qty > self.produce_per_turn:
                price = last_price * ((100 - self.price_rate) / 100)
            else:
                price = last_price * ((100 + self.price_rate) / 100)

        return price

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return self.name

    def info(self):
        return "{} Prod:{}-{} Good:{}-{} Money:{} ".format(self.name, self.product, self.product_qty, self.good,
                                                           self.good_qty, self.money)


class Demand:
    def __init__(self, consumer, good, money):
        self.consumer = consumer
        self.good = good
        self.money = money

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return "Consumer:{} Good:{} Money:{} ".format(self.consumer, self.good, self.money)


class Offer:
    def __init__(self, producer, product, qty, price):
        self.producer = producer
        self.product = product
        self.qty = qty
        self.price = price

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return "Producer:{} Product:{} Qty:{} Price:{}".format(self.producer, self.product, self.qty, self.price)


class Deal:
    def __init__(self, seller, buyer, product, price, qty):
        self.seller = seller
        self.buyer = buyer
        self.product = product
        self.price = price
        self.qty = qty

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return "Seller:{} Buyer:{} Product:{} Price:{} Qty:{}".format(self.seller, self.buyer, self.product, self.price,
                                                                      self.qty)


class Eco:
    def __init__(self):
        self.step = 0
        self.agents = []
        self.demands = []
        self.offers = []
        self.deals = []
        self.deals_history = []

    def init(self, number_agents, money, produce_per_turn):
        money_agent = int(money / number_agents)

        for count in range(number_agents):
            if count % 2 == 0:
                product = Product.A
                consumed = Product.B
            else:
                product = Product.B
                consumed = Product.A

            name = "Agent#{}".format(count + 1)
            self.agents.append(EcoAgent(name, product, consumed, produce_per_turn, money_agent))

    def make_step(self):
        self.step += 1

        self.produce()
        self.trade()
        self.consume()

    def make_steps(self, steps):
        for _ in range(steps):
            self.make_step()

    def produce(self):
        for agent in self.agents:
            agent.produce()

    def trade(self):
        self.demands.clear()
        self.make_demands()

        self.offers.clear()
        self.make_offers()

        self.deals.clear()
        self.make_deals()

        self.process_deals()

    def make_demands(self):
        for agent in self.agents:
            self.demands.append(agent.get_demand())

    def make_offers(self):
        for agent in self.agents:
            if agent.product_qty > 0:
                price = agent.get_price(self.get_last_price(agent))
                self.offers.append(Offer(agent, agent.product, agent.product_qty, price))

    def make_deals(self):
        self.make_deals_with_product(Product.A)
        self.make_deals_with_product(Product.B)

    def make_deals_with_product(self, product):
        demands = list(filter(lambda d: d.good == product, self.demands))
        random.shuffle(demands)

        offers = list(filter(lambda o: o.product == product, self.offers))
        offers.sort(key=lambda o: o.price)

        index_offer = 0
        for demand in demands:
            while demand.money > 0 and index_offer <= len(offers) - 1:

                offer = offers[index_offer]
                if offer.price > 0:
                    if offer.price > demand.money:
                        break
                    else:
                        qty = demand.money // offer.price
                        money = qty * offer.price

                        self.deals.append(Deal(offer.producer, demand.consumer, product, offer.price, qty))
                        offer.qty -= qty
                        demand.money -= money

                        if offer.qty == 0:
                            index_offer += 1
                else:
                    index_offer += 1

    def process_deals(self):
        for deal in self.deals:
            money = deal.qty * deal.price

            seller = deal.seller
            seller.money += money
            seller.product_qty -= deal.qty

            buyer = deal.buyer
            buyer.money -= money
            buyer.good_qty += deal.qty

            deal_history = {'step': self.step, 'seller': seller, 'buyer': buyer, 'price': deal.price, 'qty': deal.qty,
                            'money': money}
            self.deals_history.append(deal_history)

    def consume(self):
        for agent in self.agents:
            agent.consume()

    def get_last_price(self, seller):
        deals = list(filter(lambda d: d.get('seller') == seller, self.deals_history))
        deals.sort(key=lambda e: e.get('step'), reverse=True)
        if len(deals) > 0:
            last_price = deals[0].get('price')
        else:
            last_price = None

        return last_price

    def print_agents_info(self):
        for agent in self.agents:
            print(agent.info())


def main():
    eco = Eco()
    eco.init(number_agents=2, money=100, produce_per_turn=2)
    eco.make_steps(3)

    eco.print_agents_info()
    print(eco.deals_history)


if __name__ == '__main__':
    main()
