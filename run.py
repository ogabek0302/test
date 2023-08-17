import requests
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    merchant = Column(String)
    image_width = Column(Integer)
    image_height = Column(Integer)
    image_url = Column(String)

    attributes = relationship("Attribute", back_populates="offer")

class Attribute(Base):
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    offer_id = Column(Integer, ForeignKey('offers.id'))

    offer = relationship("Offer", back_populates="attributes")

response = requests.get("https://www.kattabozor.uz/hh/test/api/v1/offers")
response.encoding = 'utf-8'  # Устанавливаем кодировку

data = response.json()["offers"]

engine = create_engine('sqlite:///offers.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

for item in data:
    offer = Offer(
        id=item["id"],
        name=item["name"],
        brand=item["brand"],
        category=item["category"],
        merchant=item["merchant"],
        image_width=item["image"]["width"],
        image_height=item["image"]["height"],
        image_url=item["image"]["url"],
        attributes=[]
    )

    for attr in item["attributes"]:
        attribute = Attribute(name=attr["name"], value=attr["value"])
        offer.attributes.append(attribute)

    session.add(offer)

session.commit()


# Продолжение предыдущего кода

# Извлекаем все предложения (offers) из базы данных
all_offers = session.query(Offer).all()

for offer in all_offers:
    print("-" * 50)
    print(f"ID: {offer.id}")
    print(f"Name: {offer.name}")
    print(f"Brand: {offer.brand}")
    print(f"Category: {offer.category}")
    print(f"Merchant: {offer.merchant}")
    print(f"Image: {offer.image_url}")
    
    print("Attributes:")
    for attribute in offer.attributes:
        print(f"   {attribute.name}: {attribute.value}")

print("-" * 50)
