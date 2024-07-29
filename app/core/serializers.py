from users.models import User
from .models import Enter, Order, WorkerProduct, Message, WorkerWork, Expense, CompanyProduct, \
    WorkerProductGet, CompanyName, Sold, FinishedProduct, CompanyBalance, WorkerExpense, WorkerProductSendAdmin, \
    TestOrder, OrderAssignment, WorkerProductOrder
from rest_framework import serializers
from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Enter
        fields = ('id', 'name', 'qty', 'price', 'total_price', 'ndc_price', 'ndc',
                  'created_at', 'dollor_course_total', 'dollor_course', 'measurement', 'description',
                  'category', 'STIR', 'company_name', 'payment_price')
        extra_kwargs = {'payment_price': {'required': False}}


class CompanyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProduct
        fields = ['id', 'name', 'price', 'image', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'name', 'status', 'qty',
                   'work_proses', 'created_at',
                   'description', 'measurement', 'price', 'image', 'worker_data', 'worker_salary')
        extra_kwargs = {'worker_data': {'required': False},
                        'image': {'required': False}}


class WorkerProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = WorkerProduct
        fields = ('id', 'worker', 'product', 'qty', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'worker', 'order', 'text', 'created_at')


class AllMessageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'order', 'text', 'created_at')


class WorkerOrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    order = OrderSerializer()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'worker', 'order', 'text', 'created_at')


class WorkerWorkSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    worker = UserSerializer()

    class Meta:
        model = WorkerWork
        fields = '__all__'


class FilterDateSerializer(serializers.Serializer):
    startDate = serializers.DateTimeField()
    endDate = serializers.DateTimeField()


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'worker', 'price', 'status', 'description', 'created_at',]
        extra_kwargs = {'worker': {'required': False}, 'user': {'required': False}}


class ExpenseGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    worker = UserSerializer()

    class Meta:
        model = Expense
        fields = ['id', 'user', 'worker', 'price', 'status',  'description', 'created_at']




class WorkerProductGetSerializer(serializers.ModelSerializer):
    worker = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = WorkerProductGet
        fields = ['id', 'worker', 'product', 'qty', 'created_at', 'user']


class FinishedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinishedProduct
        fields = ['id', 'order', 'work_proses', 'product',   'created_at']


class OrderSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'name', 'status', 'qty',
                   'work_proses', 'created_at',
                   'description', 'measurement', 'price')
        extra_kwargs = {'worker_data': {'required': False},
                        'image': {'required': False}}


class FinishedProductGetSerializer(serializers.ModelSerializer):
    order = OrderSerializer1()
    product = ProductSerializer()

    class Meta:
        model = FinishedProduct
        fields = ['id', 'order', 'work_proses', 'created_at', 'product']


class SoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sold
        fields = ['id', 'qty', 'price', 'ndc', 'STIR', 'company_name',  'total_price',
                  'ndc_price', 'worker_product_order']


class SoldGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sold
        fields = ['id', 'qty', 'price', 'ndc', 'STIR', 'company_name',
                  'total_price', 'ndc_price', 'worker_product_order', 'payment_price']
        extra_kwargs = {'payment_price': {'required': False}}


class CompanyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBalance
        fields = ['id', 'company', 'price', 'dollar_course',  'created_at']


class CompanyNameSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sold = SoldSerializer()

    class Meta:
        model = CompanyName
        fields = ['id', 'STIR', 'company_name', 'product', 'sold',  'balance', 'created_at']


class CompanyBalanceGetSerializer(serializers.ModelSerializer):
    company = CompanyNameSerializer()

    class Meta:
        model = CompanyBalance
        fields = ['id', 'company', 'price', 'dollar_course', 'created_at']


class WorkExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerExpense
        fields = ['id', 'worker',  'price', 'created_at']


class CompanyNameProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CompanyName
        fields = ['id', 'STIR', 'company_name', 'product', 'balance']


class CompanyNameSoldSerializer(serializers.ModelSerializer):
    sold = SoldSerializer()

    class Meta:
        model = CompanyName
        fields = ['id', 'STIR', 'company_name', 'sold', 'balance', 'created_at']


class WorkerProductSendAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerProductSendAdmin
        fields = ['id', 'worker', 'qty',  'product', 'status', 'created_at']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class ProductSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Enter
        fields = ['id', 'name', 'qty', 'measurement']


class WorkerProductSendGetAdminSerializer(serializers.ModelSerializer):
    product = ProductSerializer1()
    worker = WorkerSerializer()

    class Meta:
        model = WorkerProductSendAdmin
        fields = ['id', 'qty',  'product', 'worker', 'status', 'created_at']


class OrderAssignmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = OrderAssignment
        fields = ['id', 'user', 'qty']


class TestOrderSerializer(serializers.ModelSerializer):
    assignments = OrderAssignmentSerializer(many=True, required=False)

    class Meta:
        model = TestOrder
        fields = ['id', 'name', 'description', 'assignments']

    def create(self, validated_data):
        assignments_data = validated_data.pop('assignments', [])
        test_order = TestOrder.objects.create(**validated_data)
        for assignment_data in assignments_data:
            OrderAssignment.objects.create(order=test_order, **assignment_data)
        return test_order

    def update(self, instance, validated_data):
        assignments_data = validated_data.pop('assignments', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        keep_assignments = []
        for assignment_data in assignments_data:
            if 'id' in assignment_data.keys():
                if OrderAssignment.objects.filter(id=assignment_data['id']).exists():
                    assignment = OrderAssignment.objects.get(id=assignment_data['id'])
                    assignment.user = assignment_data.get('user', assignment.user)
                    assignment.qty = assignment_data.get('qty', assignment.qty)
                    assignment.save()
                    keep_assignments.append(assignment.id)
                else:
                    continue
            else:
                assignment = OrderAssignment.objects.create(order=instance, **assignment_data)
                keep_assignments.append(assignment.id)

        for assignment in instance.assignments.all():
            if assignment.id not in keep_assignments:
                assignment.delete()

        return instance


class BulkWorkerProductOrderSerializer(serializers.Serializer):
    finish_product = serializers.UUIDField()
    qty = serializers.IntegerField()
    product_name = serializers.CharField()


class WorkerProductOrderSerializer(serializers.ModelSerializer):
    products = BulkWorkerProductOrderSerializer(many=True)

    class Meta:
        model = WorkerProductOrder
        fields = ['name', 'product_qty', 'products']


class WorkerProductOrderDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    product_qty = serializers.IntegerField()
    products = BulkWorkerProductOrderSerializer(many=True)


class WorkerProductOrderDetailSerializer1(serializers.ModelSerializer):
    products = FinishedProductSerializer(many=True, read_only=True)

    class Meta:
        model = WorkerProductOrder
        fields = ('id', 'name', 'product_qty', 'products')
