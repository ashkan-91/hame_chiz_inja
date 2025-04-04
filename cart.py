from shop.models import Product, Profile

class Cart:  
    def __init__(self, request):  
        self.session = request.session 
        self.request = request

        cart = self.session.get('session_key')  
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}  
        self.cart = cart  
    
    def db_add(self, product, quantity):  
        product_id = str(product)  
        quantity = int(quantity)  

        if product_id in self.cart:  
            self.cart[product_id] += quantity  # اضافه کردن به مقدار قبلی  
        else:  
            self.cart[product_id] = quantity  
        self.session.modified = True 

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            db_cart = str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))

    def add(self, product, quantity):  
        product_id = str(product.id)  
        quantity = int(quantity)  

        if product_id in self.cart:  
            self.cart[product_id] += quantity  # اضافه کردن به مقدار قبلی  
        else:  
            self.cart[product_id] = quantity  
        self.session.modified = True 

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            db_cart = str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))

    def __len__(self):  
        return len(self.cart)  # تعداد کل محصولات در سبد خرید  

    def get_prods(self):  
        product_ids = self.cart.keys()  
        products = Product.objects.filter(id__in=product_ids)  
        return products  

    def get_quants(self):  
        return self.cart

    def cart_total(self):  
        total = 0  
        product_ids = self.cart.keys()  
        products = Product.objects.filter(id__in=product_ids)  

        for product in products:  
            quantity = self.cart[str(product.id)]  
            if product.is_sale:  
                total += product.sale_price * quantity
            elif product.is_good_sale:  
                total += product.sale_price * quantity

            else:  
                total += product.price * quantity  

        return total  

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            db_cart = str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))
        ashkan = self.cart
        return ashkan  

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            db_cart = str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))  