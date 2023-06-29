from django.db import models
#########################################
from django.contrib.auth.models import User


class Customer(models.Model):
    class Meta:
        verbose_name = 'مشتری '
        verbose_name_plural = 'مشتری'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='حساب کاربری')
    # important fields that are stored in User model:
    #   first_name, last_name, email, date_joined

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = ((MALE, 'مرد'), (FEMALE, 'زن'))
    gender = models.IntegerField('جنسیت', choices=GENDER_CHOICES, blank=True)

    address = models.TextField('آدرس', blank=True)
    mobile = models.CharField('تلفن همراه', max_length=11)
    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    profile_image = models.ImageField('تصویر', upload_to='profile_images/', null=True, blank=True)
    balance = models.IntegerField('اعتبار', default=0)

    def __str__(self):
        return self.user.get_full_name()

    def get_balance_display(self):
        return '{:,} تومان'.format(self.balance)

    # behaviors
    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        return True


class Product(models.Model):
    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا'

    ProductName = models.CharField('نام کالا', max_length=50)
    ProductPrice = models.IntegerField('قیمت')

    ProductImage = models.ImageField('تصویر', upload_to='product_images/')
    # TODO:New Field #
    ProductStock = models.IntegerField('موجودی کالا')
    ProductDescription = models.TextField('توضیح مخنصری در مورد کالا')

    Available = 1
    NotAvailable = 0
    status_choices = (
        (Available, 'موجود در انبار'),
        (NotAvailable, 'موجودی تا چند روز آینده'),
    )
    ProductStatus = models.IntegerField('وضعیت', choices=status_choices)

    def get_price_display(self):
        return '{:,} تومان'.format(self.ProductPrice)

    def __str__(self):
        return F"{self.ProductName} - {self.ProductPrice}"

    def reserve_stock(self, sell_count):
        assert isinstance(sell_count, int) and sell_count > 0, 'Number of sells should be a positive integer'
        assert self.ProductStatus == Product.Available, 'Product is not Available'
        assert self.ProductStock >= sell_count, 'Not enough ProductStock'
        self.ProductStock -= sell_count
        if self.ProductStock == 0:
            self.ProductStatus = Product.NotAvailable
        self.save()


class OrderApp(models.Model):
    class Meta:
        verbose_name = 'سفارشات '
        verbose_name_plural = 'سفارشات'

    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='کالا')
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='خریدار')
    sell_count = models.IntegerField('تعداد خرید')
    order_time = models.DateTimeField('تاریخ ثبت سفارش', auto_now_add=True)

    def __str__(self):
        return "{} سفارش به نام {} برای کالای {}".format(self.sell_count, self.customer, self.product)


class Payment(models.Model):
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.PositiveIntegerField('مبلغ')
    transaction_time = models.DateTimeField('زمان تراکنش', auto_now_add=True)
    transaction_code = models.CharField('رسید تراکنش', max_length=30)

    def get_amount_display(self):
        return '{:,} تومان'.format(self.amount)

    def __str__(self):
        return '{:20,} تومان افزایش اعتبار برای {}'.format(self.amount, self.customer)
