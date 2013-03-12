from neomodel.traversal import Traversal, Query
from neomodel import (StructuredNode, RelationshipTo, StringProperty, OUTGOING)


class Shopper(StructuredNode):
    name = StringProperty(unique_index=True)
    friend = RelationshipTo('Shopper', 'FRIEND')
    basket = RelationshipTo('Basket', 'ITEM')


class Basket(StructuredNode):
    item = RelationshipTo('ShoppingItem', 'ITEM')


class ShoppingItem(StructuredNode):
    name = StringProperty()


def setup_shopper(name):
    jim = Shopper(name=name).save()
    b = Basket().save()
    si1 = ShoppingItem(name='Tooth brush').save()
    si2 = ShoppingItem(name='Screwdriver').save()
    b.item.connect(si1)
    b.item.connect(si2)
    jim.basket.connect(b)
    return jim


def test_one_level_traversal():
    jim = setup_shopper('Jim')
    t = Traversal(jim)
    t.traverse('friend')
    t.execute()
    from pprint import pprint as pp
    pp(t.query)
    assert t.query[-1]['return'][0] is 'friend'
    assert t.query[-2]['name'] == 'friend'
    assert t.query[-2]['direction'] is OUTGOING
    print Query(t.query)


def test_multilevel_traversal():
    bill = setup_shopper('bill')
    t = Traversal(bill)
    t.traverse('friend').traverse('basket')
    t.execute()
    from pprint import pprint as pp
    pp(t.query)
    print Query(t.query)
