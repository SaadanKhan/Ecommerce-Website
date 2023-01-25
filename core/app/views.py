from django.shortcuts import render,redirect
from .models import Category,Product,Order
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Customer,Product
from django.contrib.auth.hashers import make_password, check_password
from django.views import View



class Signup(View):

       def get(self,request):
              return render(request,'signup.html')
       
       def post(self,request):
              first_name = request.POST.get('firstname')
              last_name = request.POST.get('lastname')
              email = request.POST.get('email')
              phone = request.POST.get('phone')
              password = request.POST.get('password')
              Con_pass = request.POST.get('Con_pass')
              
              # In case of error, our fields will not be empty again
              values = {
                     'fname':first_name,
                     'lname':last_name,
                     'email':email,
                     'phone':phone
              }

              # ---------Checking the length of phone number-----------
              if len(phone) <= 10:
                     error = "Phone number must be of length 11"
                     data = {
                            'error':error,
                            'value':values
                     }
                     return render(request, "signup.html",data)

              # ---------Both passwords must be equal--------------
              elif password == Con_pass:
                     # Password hashing
                     password = make_password(password)
                     if len(password) <= 6:
                            error = "Password with minimum length of 6 allowed"
                            data = {
                            'error':error,
                            'value':values
                            }
                            return render(request, "signup.html",data)
                     else:
                            customer = Customer(
                                          first_name=first_name,
                                          phone=phone,
                                          email=email,
                                          password=password,
                                          last_name=last_name
                                   )

                            # --------Checking the email in database---------
                            # isExist()----- Function we have made in models file
                            if customer.isExist():
                                   error = "**Email already exists"
                                   data = {
                                          'error':error,
                                          'value':values
                                          }
                                   return render(request, "signup.html",data)
                            else:
                                   customer.save()
                                   return redirect('home')                                  
              else:
                     error = "Passwords must be same"
                     data = {
                            'error':error,
                            'value':values
                     }
                     return render(request, "signup.html",data)                     


class Home(View):

       def get(self,request):
              cart = Category.get_all_category()
              id_data_to_fetch = request.GET.get('category_id')

              if id_data_to_fetch:
                     product = Product.get_all_products_category(id_data_to_fetch)
                     print(product)
              else:
                     product = Product.get_all_products_static()         
              data = {}
              data['products'] = product
              data['carts'] = cart    

              return render(request , 'home.html', data)


       def post(self,request):
              product = request.POST.get('product_id')
              remove = request.POST.get('remove')
              cart = request.session.get('cart')
              if cart:
                     quantity = cart.get(product)
                     if quantity:
                            if remove:
                                   if quantity == 1:
                                          cart.pop(product)
                                   else:
                                          cart[product] = quantity - 1
                            else:
                                   cart[product] = quantity + 1
                     else:
                            cart[product] = 1
              else:
                     cart = {}
                     cart[product] = 1
              
              request.session['cart'] = cart
              print(cart)
              return redirect('home')


class Login(View):

       def get(self, request):
              return render(request,'login.html')

       def post(self,request):
              
              email = request.POST.get('email')
              password = request.POST.get('password')

              customer = Customer.get_email(email)
              error = None
              if customer:
                     
                     # Check_password will always take two parameters
                     # password we got from the form and the password we have saved in database
                     # in this case we are getting our model Customer in "customer"
                     flag = check_password(password , customer.password)

                     if flag:
                     # Add the customer data to sessions
                            request.session['customer_id'] = customer.id
                            request.session['customer_email'] = customer.email

                            return redirect('home')
                     else:
                            error = "**Password or email is invalid"
              
              else:
                     error = "**Password or email is invalid"

              return render(request, 'login.html', {'error':error})

def logout(request):

       request.session.clear()
       return redirect ('login')


class Cart(View): 
       def get(self, request):
              ids = list(request.session.get('cart').keys())
              products = Product.get_products_by_id(ids)
              return render(request,'cart.html', {'products':products})


class Checkout(View): 
       def post(self, request):
              # I have made customer session by its id which is "customer_id" in login function
              customer = request.session.get('customer_id')
              cart = request.session.get('cart')

              products = Product.get_products_by_id(list(cart.keys()))

              for product in products:
                     
                     order = Order(customer=Customer(id=customer),
                            product=product,
                            price=product.price,
                            quantity=cart.get(str(product.id)))
              order.save()
              return redirect('cart')
