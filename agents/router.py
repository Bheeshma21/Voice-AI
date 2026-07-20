from agents.product_agent import ProductAgent
from agents.pricing_agent import PricingAgent
from agents.delivery_agent import DeliveryAgent
from agents.order_agent import OrderAgent


class RouterAgent:

    def __init__(self):
        self.product = ProductAgent()
        self.pricing = PricingAgent()
        self.delivery = DeliveryAgent()
        self.order = OrderAgent()

    def route(self, query):

        query = query.lower()

        if any(word in query for word in
               ["price", "cost", "offer", "discount"]):
            return self.pricing.handle(query)

        elif any(word in query for word in
                 ["delivery", "shipping", "arrive"]):
            return self.delivery.handle(query)

        elif any(word in query for word in
                 ["order", "buy", "cart"]):
            return self.order.handle(query)

        return self.product.handle(query) 
