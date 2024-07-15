from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData,Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import validates,relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    # add relationship
    restaurant_pizzas = relationship('RestaurantPizza', backref='restaurant', cascade="all, delete-orphan")
    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant', '-restaurant_pizzas.pizza')
    
    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)

    # add relationship
    restaurant_pizzas = relationship('RestaurantPizza', backref='pizza', cascade="all, delete-orphan")

    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza', '-restaurant_pizzas')
    
    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    pizza_id = Column(Integer, ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)

    # add serialization rules
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    # add validation
    @validates('price')
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("Price must be between 1 and 30")
        return value



    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
