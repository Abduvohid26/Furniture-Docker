import uuid
from django.db import models
from django.db.models import Sum

from shared.models import BaseModel
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users.utils import validate_image
from users.models import User
from django.db import transaction
CONFIRMED, NO_CONFIRMED, REJECT = ('CONFIRMED', 'NO_CONFIRMED', 'REJECT')

# from django.contrib.auth import get_user_model
# User = get_user_model()


class Enter(BaseModel):
    Measurement = (
        ('dona', 'dona'),
        ('m3', 'm3'),
        ('m2', 'm2'),
        ('sum', 'sum'),
        ('kg', 'kg'),
        ('g', 'g'),
        ('l', 'l'),
        ('m', 'm'),
        ('complekt', 'complekt'),
        ('banka', 'banka'),
        ('list', 'list'),
        ('tonna', 'tonna'),
        ('pochka', 'pochka')
    )
    CATEGORY = (
        ('mahsulot', 'mahsulot'),
        ('homashyo', 'homashyo'),
        ('finished_product', 'finished_product')
    )
    name = models.CharField(max_length=255)
    qty = models.FloatField()
    price = models.PositiveIntegerField()
    ndc = models.PositiveIntegerField(default=12)
    measurement = models.CharField(max_length=100, choices=Measurement, default='kg')
    dollor_course = models.PositiveIntegerField()
    description = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY, default='mahsulot')
    STIR = models.CharField(max_length=14)
    company_name = models.CharField(max_length=1000)
    payment_price = models.IntegerField(default=0)

    @property
    def total_price(self):
        if self.price:
            total = self.price * self.qty
            return total

    @property
    def ndc_price(self):
        if self.total_price:
            ndc_rate = self.total_price * self.ndc // 100
            return self.total_price + ndc_rate

    @property
    def dollor_course_total(self):
        if self.dollor_course:
            dollor_course_t = self.ndc_price // self.dollor_course
            return dollor_course_t

    def __str__(self):
        return f"{self.name} qty-> {self.qty}"

    # def create_company_name(self):
    #     company = CompanyName.objects.get(STIR=self.STIR)
    #     if company is not None:
    #         company.balance += self.payment_price - self.total_price
    #         company.save()
    #     else:
    #         balance = -self.total_price if self.payment_price == 0 else self.payment_price - self.total_price
    #         CompanyName.objects.create(product_id=self.id, STIR=self.STIR,
    #                                    company_name=self.company_name, balance=balance)

    def create_company_name(self):
        try:
            company = CompanyName.objects.get(STIR=self.STIR)
        except CompanyName.DoesNotExist:
            balance = -self.ndc_price if self.payment_price == 0 else self.payment_price - self.ndc_price
            CompanyName.objects.create(product_id=self.id, STIR=self.STIR, company_name=self.company_name,
                                       balance=balance)
        else:
            total = self.payment_price - self.ndc_price
            company.balance += total
            company.save()

            return company

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_company_name()


class Order(BaseModel):
    ORDER_STATUS = (
        ('NO_ACTIVE', 'no_active'),
        ('PENDING', 'pending'),
        ('SUCCESSFULLY', 'successfully'),
        ('ONE_PENDING', 'ONE_PENDING'),
        ('SOLD', 'SOLD')
    )
    ORDER_MEAS = (
        ('dona', 'dona'),
        ('m3', 'm3'),
        ('m2', 'm2'),
        ('sum', 'sum'),
        ('kg', 'kg'),
        ('l', 'l'),
        ('m', 'm'),
        ('complekt', 'complekt'),
        ('banka', 'banka'),
        ('list', 'list'),
        ('tonna', 'tonna'),
        ('pochka', 'pochka'),
        ('g', 'g'),
    )
    name = models.CharField(max_length=1255)
    status = models.CharField(max_length=200, choices=ORDER_STATUS, default='NO_ACTIVE')
    work_proses = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField()
    description = models.TextField()
    measurement = models.CharField(max_length=100, choices=ORDER_MEAS, default='dona')
    price = models.PositiveIntegerField()
    image = models.CharField(max_length=1000, null=True, blank=True)
    worker_data = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.qty}'

    @property
    def worker_salary(self):
        if self.price and self.work_proses:
            return self.price * int(self.work_proses)


class WorkerProduct(BaseModel):
    product = models.ForeignKey(Enter, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.FloatField()

    def __str__(self):
        return self.worker.username


class WorkerProductSendAdmin(BaseModel):
    STATUS = (
        (CONFIRMED, CONFIRMED),
        (NO_CONFIRMED, NO_CONFIRMED),
        (REJECT, REJECT)
    )
    product = models.ForeignKey(Enter, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.FloatField()
    status = models.CharField(max_length=100, choices=STATUS, default=NO_CONFIRMED)

    def __str__(self):
        return self.worker.username


class WorkerProductGet(BaseModel):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Enter, on_delete=models.CASCADE)
    qty = models.IntegerField()


@receiver(signal=post_save, sender=WorkerProduct)
def worker_product_create(sender, created, instance, **kwargs):
    if created:
        WorkerProductGet.objects.create(worker=instance.worker, product=instance.product, qty=instance.qty)


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_messages')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_messages')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.worker} and {self.order}'


class WorkerWork(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='worker_work_orders')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_work')


@receiver(signal=post_save, sender=Message)
def create_work(sender, created, instance, **kwargs):
    if created:
        WorkerWork.objects.create(order=instance.order, worker=instance.worker)


class Expense(BaseModel):
    EXPENSE_STATUS = (
        ('MATERIAL_COST', 'MATERIAL_COST'),
        ('SALARY', 'SALARY'),
        ('TRANSPORT', 'TRANSPORT'),
        ('OKLAD_PAYMENT', 'OKLAD_PAYMENT'),
        ('OTHER', 'OTHER')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_expense', null=True, blank=True)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_expense', null=True, blank=True)
    status = models.CharField(max_length=204, choices=EXPENSE_STATUS, default='MATERIAL_COST')
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.user)


class WorkerExpense(BaseModel):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_exp')
    price = models.IntegerField()

    def __str__(self):
        return str(self.worker)


@receiver(pre_save, sender=WorkerProduct)
def save_old_instance(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = WorkerProduct.objects.get(pk=instance.pk)
        except WorkerProduct.DoesNotExist:
            instance._old_instance = None


@receiver(post_save, sender=WorkerProduct)
def process_worker_product_changes(sender, instance, created, **kwargs):
    total_price = instance.qty * instance.product.price
    worker = instance.worker

    if created:
        WorkerExpense.objects.create(worker=worker, price=total_price)
    else:
        old_instance = getattr(instance, '_old_instance', None)
        if old_instance is not None:
            old_total_price = old_instance.qty * old_instance.product.price
            price_difference = total_price - old_total_price
        else:
            price_difference = total_price

        worker_expense_qs = WorkerExpense.objects.filter(worker=worker)
        if worker_expense_qs.exists():
            worker_expense_total = worker_expense_qs.aggregate(total=Sum('price'))['total']
            new_total_price = worker_expense_total + price_difference
            worker_expense_qs.update(price=new_total_price)
        else:
            WorkerExpense.objects.create(worker=worker, price=total_price)

    # Check if Expense exists for the worker
    expense, created_exp = Expense.objects.get_or_create(
        worker=worker,
        status='MATERIAL_COST',
        defaults={
            'price': total_price,
            'description': 'Buyurtma bajarish uchun olindi'
        }
    )
    if not created_exp:
        expense.price = WorkerExpense.objects.filter(worker=worker).aggregate(total=Sum('price'))['total']
        expense.save()


@receiver(pre_save, sender=WorkerExpense)
def save_old_worker_expense_instance(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = WorkerExpense.objects.get(pk=instance.pk)
        except WorkerExpense.DoesNotExist:
            instance._old_instance = None


@receiver(post_save, sender=WorkerExpense)
def update_expense_on_worker_expense_change(sender, instance, created, **kwargs):
    if created or getattr(instance, '_old_instance', None):
        total_expense_price = WorkerExpense.objects.filter(worker=instance.worker).aggregate(total=Sum('price'))['total']
        expense, created_exp = Expense.objects.get_or_create(
            worker=instance.worker,
            status='MATERIAL_COST',
            defaults={
                'price': total_expense_price,
                'description': 'Buyurtma bajarish uchun olindi'
            }
        )
        if not created_exp:
            expense.price = total_expense_price
            expense.save()


# @receiver(post_save, sender=WorkerExpense)
# def update_expense_on_worker_expense_change(sender, instance, created, **kwargs):
#     total_expense_price = WorkerExpense.objects.filter(worker=instance.worker).aggregate(total=Sum('price'))['total']
#     # Yangi Expense yaratmasdan, eski Expense yangilanadi
#     expense = Expense.objects.filter(worker=instance.worker, status='MATERIAL_COST').first()
#     if expense:
#         expense.price = total_expense_price
#         expense.save()
#     else:
#         Expense.objects.create(
#             worker=instance.worker,
#             status='MATERIAL_COST',
#             price=total_expense_price,
#             description='Buyurtma bajarish uchun olindi'
#         )


class CompanyProduct(BaseModel):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    image = models.ImageField(default='default_order.png', upload_to='company-images/%d/',
                              validators=[validate_image])

    def __str__(self):
        return self.name


class Sold(BaseModel):
    worker_product_order = models.ForeignKey('core.WorkerProductOrder', on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    ndc = models.PositiveIntegerField(default=12)
    STIR = models.CharField(max_length=14, blank=True, null=True)
    company_name = models.CharField(max_length=1000, blank=True, null=True)
    payment_price = models.IntegerField(default=0)

    @property
    def total_price(self):
        if self.qty and self.price:
            return self.qty * self.price
        return None

    @property
    def ndc_price(self):
        if self.total_price:
            ndc_rate = self.total_price * self.ndc // 100
            return self.total_price + ndc_rate

    def __str__(self):
        return str(self.company_name)

    def create_company_name(self):
        try:
            company = CompanyName.objects.get(STIR=self.STIR, company_name=self.company_name)
        except CompanyName.DoesNotExist:
            balance = self.qty * self.price
            CompanyName.objects.create(
                sold=self,
                STIR=self.STIR,
                company_name=self.company_name,
                balance=balance
            )
        else:
            company.balance += self.qty * self.price
            company.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_company_name()


class CompanyName(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    STIR = models.CharField(max_length=14)
    company_name = models.CharField(max_length=1000)
    sold = models.ForeignKey(Sold, on_delete=models.SET_NULL, null=True, blank=True, related_name='company')
    product = models.ForeignKey(Enter, on_delete=models.CASCADE, null=True, blank=True, related_name='company_names')
    balance = models.IntegerField()

    def __str__(self):
        return f'{self.company_name} {self.STIR}'


class FinishedProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Enter, on_delete=models.CASCADE, null=True, blank=True)
    work_proses = models.IntegerField()

    def __str__(self):
        return f'{self.order} {self.product}'


@receiver(signal=post_save, sender=Enter)
def finish_product_create(sender, created, instance, **kwargs):
    if created and instance.category == 'finished_product':
        FinishedProduct.objects.create(order=None, product=instance, work_proses=instance.qty)


class CompanyBalance(BaseModel):
    company = models.ForeignKey(CompanyName, on_delete=models.CASCADE)
    price = models.IntegerField()
    dollar_course = models.IntegerField(default=0)

    def __str__(self):
        return str(self.company.company_name)


class TestOrder(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    workers = models.ManyToManyField(User, through='OrderAssignment', related_name='test_orders')

    def __str__(self):
        return self.name


class OrderAssignment(models.Model):
    order = models.ForeignKey(TestOrder, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.name} - {self.user.username} - Qty: {self.qty}"

# BaseModel add kerak rm bolganda


class WorkerProductOrder(models.Model):
    name = models.CharField(max_length=255)
    product_qty = models.IntegerField()
    finish_product = models.ForeignKey(FinishedProduct, on_delete=models.CASCADE)
    qty = models.IntegerField()
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
