from enum import Enum, auto
import random


class Product(Enum):
    A = auto()
    B = auto()

    def __str__(self):
        return self.name


class EcoAgent:
    def __init__(self, name, product, good, produce_per_turn, consume_per_turn, money):
        self.name = name
        self.product = product
        self.good = good
        self.money = money
        self.produce_per_turn = produce_per_turn
        self.consume_per_turn = consume_per_turn
        self.product_qty = 0
        self.good_qty = 0

    def produce(self):
        self.product_qty += self.produce_per_turn

    def consume(self):
        consumed = min(self.good_qty, self.consume_per_turn)
        self.good_qty -= consumed

    def get_demand(self):
        return Demand(self, self.good, self.money)

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
    def __init__(self, consumer, good, amount):
        self.consumer = consumer
        self.good = good
        self.amount = amount

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return "Consumer:{} Good:{} Amount:{} ".format(self.consumer, self.good, self.amount)


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


class Eco:
    def __init__(self):
        self.turn = 0
        self.agents = []
        self.demands = []
        self.offers = []
        self.deals = []

    def init(self, number_agents, money, produce_per_turn, consume_per_turn):
        money_agent = int(money / number_agents)

        for count in range(number_agents):
            if count % 2 == 0:
                product = Product.A
                consumed = Product.B
            else:
                product = Product.B
                consumed = Product.A

            name = "Agent#{}".format(count + 1)
            self.agents.append(EcoAgent(name, product, consumed, produce_per_turn, consume_per_turn, money_agent))

    def make_turn(self):
        self.turn += 1
        print("Turn {}".format(self.turn))

        self.produce()
        self.trade()
        self.consume()

    def produce(self):
        for agent in self.agents:
            agent.produce()

    def trade(self):
        self.demands.clear()
        self.make_demands()
        print(self.demands)

        self.offers.clear()
        self.make_offers()
        print(self.offers)

        self.deals.clear()
        self.make_deals()
        print(self.deals)

    def make_demands(self):
        for agent in self.agents:
            self.demands.append(agent.get_demand())

    def make_offers(self):
        for agent in self.agents:
            if agent.product_qty > 0:
                price = 10
                self.offers.append(Offer(agent, agent.product, agent.product_qty, price))

    def make_deals(self):
        self.offers.sort(key=lambda offer: offer.price)
        random.shuffle(self.demands)
        for demand in self.demands:
            if demand.amount <= 0:
                continue
            pass

    def consume(self):
        for agent in self.agents:
            agent.consume()

    def print_agents_info(self):
        for agent in self.agents:
            print(agent.info())


def main():
    eco = Eco()
    eco.init(10, 100, 2, 2)
    eco.make_turn()

    eco.print_agents_info()


if __name__ == '__main__':
    main()
