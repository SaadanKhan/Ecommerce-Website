# Django offers many Template tags 
# but if you want to make them for your own use you can make you can do that 
from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
       keys = cart.keys()
       # Seeing if the product is in a cart or not
       for id in keys: 
              if str(product.id)== id:
                     return True
       return False

@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    keys = cart.keys()
    for id in keys: 
              if str(product.id)== id:
                     return cart.get(id)
    return 0

@register.filter(name='total_price')
def total_price(product,cart):
       return product.price * cart_quantity(product,cart)

@register.filter(name='total_cart_price')
def total_cart_price(product,cart):
       sum = 0
       for p in product:
              sum = sum + total_price(p,cart)
       return sum