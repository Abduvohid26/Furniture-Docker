from rest_framework import status, permissions, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from users.models import WORKER, WorkStatics
from .serializers import ProductSerializer, OrderSerializer, WorkerProductSerializer, MessageSerializer, \
    AllMessageSerializer, WorkerOrderSerializer, WorkerWorkSerializer, FilterDateSerializer, \
    ExpenseSerializer, ExpenseGetSerializer, CompanyProductSerializer, WorkerProductGetSerializer, \
    CompanyNameSerializer, SoldSerializer, SoldGetSerializer, FinishedProductSerializer, \
    FinishedProductGetSerializer, CompanyBalanceSerializer, CompanyBalanceGetSerializer, WorkExpenseSerializer, \
    CompanyNameProductSerializer, CompanyNameSoldSerializer, WorkerProductSendAdminSerializer, \
    WorkerProductSendGetAdminSerializer, TestOrderSerializer, OrderAssignmentSerializer, WorkerProductOrderSerializer, \
    WorkerProductOrderDetailSerializer, WorkerProductOrderDetailSerializer

from core.models import Enter, Order, WorkerProduct, Message, WorkerWork, Expense, CompanyProduct, \
    CompanyName, Sold, FinishedProduct, CompanyBalance, WorkerExpense, WorkerProductSendAdmin, NO_CONFIRMED, REJECT, \
    TestOrder, OrderAssignment, WorkerProductOrder
from users.utils import CustomPagination
from datetime import datetime
from django.db import transaction

import uuid
from users.models import User
from users.serializers import WorkStaticGetSerializer
from rest_framework import viewsets
# from django.contrib.auth import get_user_model
# User = get_user_model()


class Product(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        products = Enter.objects.filter(qty__gt=0)
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get(self, request, id, *args, **kwargs):
        product = get_object_or_404(Enter, id=id)
        serializer = ProductSerializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, reqeust, id, *args, **kwargs):
        product = get_object_or_404(Enter, id=id)
        serializer = ProductSerializer(instance=product, data=reqeust.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, reqeust, id, *args, **kwargs):
        product = get_object_or_404(Enter, id=id)
        serializer = ProductSerializer(instance=product, data=reqeust.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            product = get_object_or_404(Enter, id=id)
        except:
            return Response(data={'errors': 'Product not found'})
        else:
            product.delete()
            return Response(data={'message': 'Product successfully deleted'})


# class OrderAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#     # pagination_class = CustomPagination
#     # def get(self, request):
#     #     order = Order.objects.all()
#     #     paginator = self.pagination_class()
#     #     page = paginator.paginate_queryset(queryset=order, request=request)
#     #     serializer = OrderSerializer(page, many=True)
#     #     response = paginator.get_paginated_response(data=serializer.data)
#     #     return Response(data=response.data, status=status.HTTP_200_OK)
#     def get(self, request, *args, **kwargs):
#         order = Order.objects.all()
#         serializer = OrderSerializer(order, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrderDetailAPIView(APIView):
#     def get(self, request, id):
#         order = get_object_or_404(Order, id=id)
#         serializer = OrderSerializer(order)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, id):
#         order = get_object_or_404(Order, id=id)
#         serializer = OrderSerializer(instance=order, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         try:
#             order = get_object_or_404(Order, id=id)
#         except:
#             return Response(data={'error': 'Order Not Fount'})

#         else:
#             order.delete()
#             return Response(data={'success': 'Order successfully deleted'})

# class OrderAPIView(generics.ListCreateAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()
#
#
# class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()


class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(order)
        return Response(data=serializer.data)

    def put(self, request, id):
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(data=request.data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(data=request.data, instance=order, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            order = get_object_or_404(Order, id=id)
        except:
            return Response(data='Order not found', status=status.HTTP_400_BAD_REQUEST)
        order.delete()
        return Response(data='Order successfully deleted', status=status.HTTP_200_OK)


class WorkerProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        worker_products = WorkerProduct.objects.all()
        serializer = WorkerProductSerializer(worker_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkerProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            worker = serializer.validated_data['worker']
            qty = serializer.validated_data['qty']
            today = datetime.today().date()  # Current date

            try:
                # Try to get WorkerProduct for the worker and product
                worker_product = WorkerProduct.objects.filter(worker=worker, product=product).first()

                if worker_product and worker_product.created_at == today:
                    # If found and created today, update the quantity
                    worker_product.qty += qty
                    worker_product.save()
                else:
                    # If not found or not created today, create a new WorkerProduct
                    serializer.save()

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct qty from Product model
            product.qty -= qty
            product.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerProductDetailAPIView(APIView):
    def get(self, request, id):
        order = get_object_or_404(WorkerProduct, id=id)
        serializer = WorkerProductSerializer(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        order = get_object_or_404(WorkerProduct, id=id)
        serializer = WorkerProductSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        order = get_object_or_404(WorkerProduct, id=id)
        serializer = WorkerProductSerializer(instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            order = get_object_or_404(WorkerProduct, id=id)
        except:
            return Response(data={'error': 'Worker_Product Not Fount'})

        else:
            order.delete()
            return Response(data={'success': 'Worker_Product successfully deleted'})


class WorkerProductAdminSendView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        worker_products = WorkerProductSendAdmin.objects.filter(status='NO_CONFIRMED')
        serializer = WorkerProductSendGetAdminSerializer(worker_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkerProductSendAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerProductAdminDetailSendView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerProductSendGetAdminSerializer
    queryset = WorkerProductSendAdmin.objects.all()
    permission_classes = [permissions.AllowAny]


class WorkerProductNoConfirmedView(APIView):
    def get(self, request, worker_id):
        worker_products = WorkerProductSendAdmin.objects.filter(worker=worker_id, status=NO_CONFIRMED)
        if not worker_products.exists():
            return Response(
                data={
                    'success': False,
                    'message': 'No unconfirmed products found for this user'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WorkerProductSendGetAdminSerializer(instance=worker_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class WorkerProductRejectView(APIView):
    def get(self, request, worker_id):
        worker_products = WorkerProductSendAdmin.objects.filter(worker=worker_id, status=REJECT)
        if not worker_products.exists():
            return Response(
                data={
                    'success': False,
                    'message': 'No reject products found for this user'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WorkerProductSendGetAdminSerializer(instance=worker_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class MessageSendAPIView(APIView):
    def get(self, request):
        order = Message.objects.all()
        serializer = MessageSerializer(order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MessageSendDetailAPIView(APIView):
    def get(self, request, id):
        order = get_object_or_404(Message, id=id)
        serializer = MessageSerializer(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        order = get_object_or_404(Message, id=id)
        serializer = MessageSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            order = get_object_or_404(Message, id=id)
        except:
            return Response(data={'error': 'Order_to_Send Not Fount'})

        else:
            order.delete()
            return Response(data={'success': 'Order_to_Send successfully deleted'})


class SendMessageView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            worker_id = serializer.validated_data.get('worker').id
            order_id = serializer.validated_data.get('order').id
            sender_id = serializer.validated_data.get('sender').id

            # Ishchini, buyurtmani va jo'natuvchini get_object_or_404 yordamida olish
            worker = get_object_or_404(User, id=worker_id)
            order = get_object_or_404(Order, id=order_id)
            sender = get_object_or_404(User, id=sender_id)

            # Buyurtma boshqa xodimga tegishli ekanligini tekshirish
            if WorkerWork.objects.filter(order=order).exclude(worker=worker).exists():
                return Response(
                    data={'success': False, 'message': 'Bu buyurtma allaqachon boshqa xodimga tegishli'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Xodim allaqachon bu buyurtmaga tayinlanganligini tekshirish
            if WorkerWork.objects.filter(order=order, worker=worker).exists():
                return Response(
                    data={'success': False, 'message': 'Bu buyurtma uchun xodim allaqachon mavjud'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Xabar yaratish
            message = Message.objects.create(sender=sender, worker=worker, order=order, text=text)

            # WorkerWork yaratish yoki mavjudligini tekshirish
            WorkerWork.objects.get_or_create(order=order, worker=worker)

            # Buyurtma holatini 'pending' ga o'zgartirish
            order.status = 'ONE_PENDING'
            order.worker_data = f'{worker.first_name} {worker.last_name}'
            order.save()
            return Response(
                data={
                    'id': message.id,
                    'success': True,
                    'message': 'Xabar muvaffaqiyatli jo\'natildi'
                }, status=status.HTTP_200_OK
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SendMessageView(APIView):
#     def post(self, request):
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             text = serializer.validated_data.get('text')
#             worker = serializer.validated_data.get('worker')
#             sender = serializer.validated_data.get('sender')
#             order_data = request.data.get('order')
#
#             # Handle Order creation or fetching
#             order = None
#             if order_data:
#                 order_id = order_data.get('id')
#                 if order_id:
#                     order = get_object_or_404(Order, id=order_id)
#                 else:
#                     # Create a new Order if order_id is not provided
#                     order = Order.objects.create(
#                         name=order_data.get('name'),
#                         status=order_data.get('status'),
#                         qty=order_data.get('qty'),
#                         price=order_data.get('price'),
#                         dollor_course=order_data.get('dollor_course'),
#                         work_proses=order_data.get('work_proses'),
#                         created_at=order_data.get('created_at'),
#                         description=order_data.get('description'),
#                         measurement=order_data.get('measurement'),
#                         STIR=order_data.get('STIR'),
#                         company_name=order_data.get('company_name'),
#                         ndc=order_data.get('ndc'),
#                         payment=order_data.get('payment')
#                     )
#
#             # Create the Message instance
#             message = Message.objects.create(sender=sender, worker=worker, order=order, text=text)
#             return Response(
#                 data={
#                     'id': message.id,
#                     'success': True,
#                     'message': 'Message successfully sent'
#                 }, status=status.HTTP_200_OK
#             )


class AllSendMessageView(APIView):
    def post(self, request):
        serializer = AllMessageSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            order = serializer.validated_data.get('order')
            sender = serializer.validated_data.get('sender')

            try:
                workers = User.objects.filter(user_roles=WORKER)
                for worker in workers:
                    worker_name = worker.username
                    print('Message', worker_name, text)

                    message = Message.objects.create(sender=sender, worker=worker, order=order, text=text)
                return Response(
                    data={
                        'id': message.id,
                        'success': True,
                        'message': 'Message successfully send'
                    }, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    data={
                        'success': False,
                        'message': 'Worker not found'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Count
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractDay

from django.utils import timezone

# class OrderStatsAPIView(APIView):
#     def get(self, request, period):
#         today = timezone.now().date()
#         start_date = end_date = None

#         if period == 'daily':
#             start_date = today
#             end_date = today + timezone.timedelta(days=1)
#         elif period == 'weekly':
#             start_date = today - timezone.timedelta(days=today.weekday())
#             end_date = start_date + timezone.timedelta(weeks=1)
#         elif period == 'monthly':
#             start_date = today.replace(day=1)
#             end_date = (start_date + timezone.timedelta(days=32)).replace(day=1)
#         elif period == 'yearly':
#             start_date = today.replace(month=1, day=1)
#             end_date = start_date.replace(year=start_date.year + 1)
#         else:
#             return Response({'error': 'Invalid period'}, status=400)

#         orders = Order.objects.filter(created_at__gte=start_date, created_at__lt=end_date)

#         # Statistikalar
#         total_orders = orders.count()
#         total_price = sum(order.total_price for order in orders)
#         avg_price = total_price / total_orders if total_orders > 0 else 0

#         return Response({
#             'period': period,
#             'total_orders': total_orders,
#             'total_price': total_price,
#             'avg_price': avg_price
#         })


WEEKDAY_NAMES = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}



@api_view(['GET'])
def weekly_order_stats(request):
    # Bugungi sana
    today = timezone.now().date()
    # Haftaning boshlang'ichidagi sana
    start_of_week = today - timedelta(days=today.weekday())
    # Haftaning oxiridagi sana
    end_of_week = start_of_week + timedelta(days=6)

    # Buyurtmalarni haftalik hisoblash
    weekly_stats = Order.objects.filter(created_at__range=[start_of_week, end_of_week]) \
                                 .values('created_at') \
                                 .annotate(total_qty=Count('id')) \
                                 .order_by('created_at')

    # Haftalik statistikani list formatida qaytaramiz
    weekly_stats_list = {'days': [], 'quantities': []}
    for stat in weekly_stats:
        created_at = stat.get('created_at')
        if created_at:
            # Haftaning nomi (Monday, Tuesday, Wednesday, etc.)
            day_number = created_at.weekday()  # 0 - dushanba, 1 - seshanba, va hokazo
            day_name = WEEKDAY_NAMES[day_number]
            # Buyurtma soni
            qty = stat['total_qty']
            # Hafta nomi va buyurtmalar sonini listga qo'shamiz
            weekly_stats_list['days'].append(day_name)
            weekly_stats_list['quantities'].append(qty)

    return Response(weekly_stats_list)


class Worker_Orders(APIView):
    def get(self, request, worker_id):
        workers = Message.objects.filter(worker=worker_id)
        serializer = WorkerOrderSerializer(workers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Worker_Orders_Delete(APIView):
    def delete(self, request, id):
        try:
            msg = Message.objects.get(id=id)
        except:
            return Response(data={'message': 'Ish not found'}, status=status.HTTP_404_NOT_FOUND)

        msg.delete()
        return Response(data={'message': 'Success'}, status=status.HTTP_200_OK)


class WorkerWorkAPIView(APIView):
    def get(self, request, worker_id):
        worker_works = WorkerWork.objects.filter(worker=worker_id)
        print(worker_id)

        if worker_works.exists():
            worker = worker_works.first().worker
        else:
            return Response(data={'message': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

        orders = []
        for worker_work in worker_works:
            order = worker_work.order
            orders.append({
                'id': order.id,
                'name': order.name,
                'status': order.status,
                'qty': order.qty,
                'work_proses': order.work_proses,
                'created_at': order.created_at,
                'description': order.description,
                'measurement': order.measurement,
                'image': order.image,
                'worker_data': order.worker_data,
                'worker_salary': order.worker_salary
            })

        custom_response = {
            'id': worker.id,
            'username': worker.username,
            'phone_number': worker.phone_number,
            'first_name': worker.first_name,
            'last_name': worker.last_name,
            'orders': orders
        }
        return Response(data=custom_response, status=status.HTTP_200_OK)


class ProductFilterDateAIView(APIView):
    def post(self, request):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            products = Enter.objects.filter(created_at__range=[start_date, end_date])
            product_serializer = ProductSerializer(products, many=True)
            return Response(data=product_serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkStaticsFilterDateAPIView(APIView):
    def post(self, request):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            work_static = WorkStatics.objects.filter(created_at__range=[start_date, end_date])
            work_static_serializer = WorkStaticGetSerializer(work_static, many=True)
            return Response(data=work_static_serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterDateAIView(APIView):
    def post(self, request):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            products = Order.objects.filter(created_at__range=[start_date, end_date])
            product_data = [
                {
                    'id': product.id,
                    'name': product.name,
                    'qty': product.qty,
                    'status': product.status,
                    'work_proses': product.work_proses,
                    'image': product.image,
                    'description': product.description,
                    'created_at': product.created_at,
                    'updated_at': product.updated_at,
                    'measurement': product.measurement
                }
                for product in products
            ]
            return Response(data=product_data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterSoldDateAIView(APIView):
    def post(self, request):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            solds = Sold.objects.filter(created_at__range=[start_date, end_date])
            custom_response = [
                {
                    'id': sold.id,
                    'qty': sold.qty,
                    'price': sold.price,
                    'ndc': sold.ndc,
                    'STIR': sold.STIR,
                    'company_name': sold.company_name,
                    'worker_product_order': {
                        'id': sold.worker_product_order.id,
                        'name': sold.worker_product_order.name,
                        'product_qty': sold.worker_product_order.product_qty,
                        'product_name': sold.worker_product_order.product_name,
                        'qty': sold.worker_product_order.qty,
                        'finish_product': {
                            'id': sold.worker_product_order.finish_product.id,
                            'work_proses': sold.worker_product_order.finish_product.work_proses
                        } if sold.worker_product_order and sold.worker_product_order.finish_product else None
                    } if sold.worker_product_order else None
                }
                for sold in solds
            ]
            return Response(data=custom_response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterSoldSTIRDateAIView(APIView):
    def post(self, request, STIR):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            products = Enter.objects.filter(STIR=STIR, created_at__range=[start_date, end_date])
            solds = Sold.objects.filter(STIR=STIR, created_at__range=[start_date, end_date])
            if products.exists():
                custom_data = [
                    {
                        'id': product.id,
                        'name': product.name,
                        'qty': product.qty,
                        'price': product.price,
                        'ndc_price': product.ndc_price,
                        'measurement': product.measurement,
                        'category': product.category,
                        'total_price': product.total_price,
                        'payment_price': product.payment_price,
                        'created_at': product.created_at,
                    }
                    for product in products
                ]
                return Response(custom_data, status=status.HTTP_200_OK)
            elif solds.exists():
                custom_data = [
                    {
                        'id': sold.id,
                        'qty': sold.qty,
                        'price': sold.price,
                        'total_price': sold.total_price,
                        'ndc_price': sold.ndc_price,
                        'payment_price': sold.payment_price,
                        'created_at': sold.created_at
                    }
                    for sold in solds
                ]
                return Response(data=custom_data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)


        #     for company_name in company_names:
        #         sold_data = {}
        #         if company_name.sold:
        #             sold_data = {
        #                 'id': company_name.sold.id,
        #                 'qty': company_name.sold.qty,
        #                 'price': company_name.sold.price,
        #                 'ndc': company_name.sold.ndc,
        #                 'total_price': company_name.sold.total_price,
        #                 'ndc_price': company_name.sold.ndc_price,
        #                 'finish_product': {}
        #             }
        #             if company_name.sold.finish_product:
        #                 sold_data['finish_product'] = {
        #                     'id': company_name.sold.finish_product.id,
        #                     'work_proses': company_name.sold.finish_product.work_proses,
        #                     'order': {}
        #                 }
        #                 if company_name.sold.finish_product.order:
        #                     sold_data['finish_product']['order'] = {
        #                         'id': company_name.sold.finish_product.order.id,
        #                         'name': company_name.sold.finish_product.order.name,
        #                         'status': company_name.sold.finish_product.order.status,
        #                         'work_proses': company_name.sold.finish_product.order.work_proses,
        #                         'qty': company_name.sold.finish_product.order.qty,
        #                         'description': company_name.sold.finish_product.order.description,
        #                         'measurement': company_name.sold.finish_product.order.measurement,
        #                         'image': company_name.sold.finish_product.order.image,
        #                     }
        #         product_data = {}
        #         if company_name.product:
        #             product_data = {
        #                 'id': company_name.product.id,
        #                 'name': company_name.product.name,
        #                 'qty': company_name.product.qty,
        #                 'price': company_name.product.price,
        #                 'ndc_price': company_name.product.ndc_price,
        #                 'measurement': company_name.product.measurement,
        #                 'category': company_name.product.category,
        #                 'created_at': company_name.product.created_at
        #             }
        #         custom_response.append({
        #             'id': company_name.id,
        #             'STIR': company_name.STIR,
        #             'company_name': company_name.company_name,
        #             'balance': company_name.balance,
        #             'sold': sold_data,
        #             'product': product_data
        #         })
        #     return Response(data=custom_response, status=status.HTTP_200_OK)
        # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterDateCostView(APIView):
    def post(self, request):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            costs = Expense.objects.filter(created_at__range=[start_date, end_date])
            custom_data = [
                {
                    'id': cost.id,
                    'price': cost.price,
                    'description': cost.description,
                    'status': cost.status,
                    'created_at': cost.created_at,
                    'user': {
                        'id': cost.user.id,
                        'username': cost.user.username,
                        'first_name': cost.user.first_name,
                        'last_name': cost.user.last_name,
                        'image': cost.user.image.url,
                        'created_at': cost.user.created_at,
                        'filial_name': cost.user.filial_name
                    }
                }
                for cost in costs
            ]
            return Response(data=custom_data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyBalanceDateFilter(APIView):
    def post(self, request):
        serializer = FilterDateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['startDate']
            end_date = serializer.validated_data['endDate']
            try:
                company_balances = CompanyBalance.objects.filter(created_at__range=[start_date, end_date])
            except Exception as e:
                return Response(
                    data={'error': str(e)},
                    status=status.HTTP_404_NOT_FOUND
                )

            custom_response = [
                {
                    'id': company_balance.id,
                    'created_at': company_balance.created_at.isoformat(),
                    'price': company_balance.price,
                    'company': {
                        'id': company_balance.company.id,
                        'STIR': company_balance.company.STIR,
                        'company_name': company_balance.company.company_name,
                        'sold': {
                            'id': company_balance.company.sold.id,
                            'qty': company_balance.company.sold.qty,
                            'price': company_balance.company.sold.price,
                            'ndc': company_balance.company.sold.ndc,
                            'total_price': company_balance.company.sold.total_price,
                            'ndc_price': company_balance.company.sold.ndc_price,
                        } if company_balance.company.sold else None,
                        'product': {
                            'id': company_balance.company.product.id,
                            'name': company_balance.company.product.name,
                            'qty': company_balance.company.product.qty,
                            'price': company_balance.company.product.price,
                            'ndc_price': company_balance.company.product.ndc_price,
                            'measurement': company_balance.company.product.measurement,
                            'category': company_balance.company.product.category,
                            'created_at': company_balance.company.product.created_at.isoformat()
                        } if company_balance.company.product else None,
                        'balance': company_balance.company.balance
                    }
                }
                for company_balance in company_balances
            ]
            return Response(data=custom_response, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CostAPIView(APIView):
    def get(self, request):
        costs = Expense.objects.all()
        serializer = ExpenseGetSerializer(instance=costs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            worker = serializer.validated_data.get('worker')
            price = serializer.validated_data.get('price')

            if worker:
                worker.salary_worker -= price
                worker.save()
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class CompanyProductAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CompanyProduct.objects.all()
    serializer_class = CompanyProductSerializer


class CompanyProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CompanyProduct.objects.all()
    serializer_class = CompanyProductSerializer


class WorkerProductGetAPIView(APIView):
    def get(self, request, worker_id):
        worker_products = WorkerProduct.objects.filter(worker_id=worker_id)

        if worker_products.exists():
            worker = worker_products.first().worker
            products = [
                {
                    'id': product.product.id,
                    'name': product.product.name,
                    'qty': product.qty,
                    'price': product.product.price * product.qty,
                    'ndc_price': product.product.ndc_price,
                    'measurement': product.product.measurement,
                    'category': product.product.category,
                    'created_at': product.product.created_at
                }
                for product in worker_products
            ]

            custom_data = {
                'id': worker.id,
                'username': worker.username,
                'phone_number': worker.phone_number,
                'first_name': worker.first_name,
                'last_name': worker.last_name,
                'products': products,
                'qty': sum(product.qty for product in worker_products),
            }

            return Response(data=custom_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No products found for this worker."}, status=status.HTTP_404_NOT_FOUND)


class WorkerProductAllGetAPIView(APIView):
    def get(self, request):
        worker_products = WorkerProduct.objects.select_related('worker', 'product').all()

        workers_dict = {}

        for worker_product in worker_products:
            worker = worker_product.worker
            product = worker_product.product

            if worker.id not in workers_dict:
                workers_dict[worker.id] = {
                    'id': worker.id,
                    'username': worker.username,
                    'phone_number': worker.phone_number,
                    'first_name': worker.first_name,
                    'last_name': worker.last_name,
                    'products': []
                }

            workers_dict[worker.id]['products'].append({
                'id': product.id,
                'name': product.name,
                'qty': worker_product.qty,
                'price': product.price,
                'ndc_price': product.ndc_price,
                'measurement': product.measurement,
                'category': product.category,
                'created_at': product.created_at
            })

        custom_data = list(workers_dict.values())

        return Response(data=custom_data, status=status.HTTP_200_OK)


class NoActiveOrder(APIView):
    def get(self, request):
        orders = Order.objects.filter(status='NO_ACTIVE')
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CompanyNameGetView(APIView):
    def get(self, request):
        company_names = CompanyName.objects.all()

        custom_response = []

        for company_name in company_names:
            sold_data = {}
            if company_name.sold:
                sold_data = {
                    'id': company_name.sold.id,
                    'qty': company_name.sold.qty,
                    'price': company_name.sold.price,
                    'ndc': company_name.sold.ndc,
                    'total_price': company_name.sold.total_price,
                    'ndc_price': company_name.sold.ndc_price,
                    'worker_product_order': {}
                }
                if company_name.sold.worker_product_order:
                    sold_data['worker_product_order'] = {
                        'id': company_name.sold.worker_product_order.id,
                        'name': company_name.sold.worker_product_order.name,
                        'product_name': company_name.sold.worker_product_order.product_name,
                        'product_qty': company_name.sold.worker_product_order.product_qty,
                        'finish_product': {}
                    }
                    # if company_name.sold.finish_product.order:
                    #     sold_data['finish_product']['order'] = {
                    #         'id': company_name.sold.finish_product.order.id,
                    #         'name': company_name.sold.finish_product.order.name,
                    #         'status': company_name.sold.finish_product.order.status,
                    #         'work_proses': company_name.sold.finish_product.order.work_proses,
                    #         'qty': company_name.sold.finish_product.order.qty,
                    #         'description': company_name.sold.finish_product.order.description,
                    #         'measurement': company_name.sold.finish_product.order.measurement,
                    #         'image': company_name.sold.finish_product.order.image,

            product_data = {}
            if company_name.product:
                product_data = {
                    'id': company_name.product.id,
                    'name': company_name.product.name,
                    'qty': company_name.product.qty,
                    'price': company_name.product.price,
                    'ndc_price': company_name.product.ndc_price,
                    'measurement': company_name.product.measurement,
                    'category': company_name.product.category,
                    'created_at': company_name.product.created_at
                }
            custom_response.append({
                'id': company_name.id,
                'STIR': company_name.STIR,
                'company_name': company_name.company_name,
                'balance': company_name.balance,
                'created_at': company_name.created_at,
                'sold': sold_data,
                'product': product_data
            })
        return Response(data=custom_response, status=status.HTTP_200_OK)


class CompanyNameView(APIView):
    def get(self, request, STIR):
        try:
            entries = list(Enter.objects.filter(STIR=STIR))
            solds = list(Sold.objects.filter(STIR=STIR))
            company_names = list(CompanyName.objects.filter(STIR=STIR))

            if entries:
                custom_data = [
                    {
                        'id': company_name.id,
                        'STIR': company_name.STIR,
                        'company_name': company_name.company_name,
                        'balance': company_name.balance,
                        'created_at': company_name.created_at,
                        'products': [
                            {
                                'id': product.id,
                                'name': product.name,
                                'qty': product.qty,
                                'price': product.price,
                                'ndc_price': product.ndc_price,
                                'measurement': product.measurement,
                                'category': product.category,
                                'total_price': product.total_price,
                                'payment_price': product.payment_price,
                                'created_at': product.created_at,
                            }
                            for product in entries
                        ]
                    }
                    for company_name in company_names
                ]
                return Response(custom_data, status=status.HTTP_200_OK)

            elif solds:
                custom_response = []
                for company_name in company_names:
                    company_info = {
                        'id': company_name.id,
                        'STIR': company_name.STIR,
                        'company_name': company_name.company_name,
                        'balance': company_name.balance,
                        'created_at': company_name.created_at,
                    }
                    for sold in solds:
                        response_item = {
                            'id': sold.id,
                            'qty': sold.qty,
                            'price': sold.price,
                            'ndc': sold.ndc,
                            'STIR': sold.STIR,
                            'company_name': sold.company_name,
                            'total_price': sold.total_price,
                            'ndc_price': sold.ndc_price,
                            'payment_price': sold.payment_price,
                            'worker_product_order': {}
                        }
                        if sold.worker_product_order:
                            worker_product_order = sold.worker_product_order
                            response_item['worker_product_order'] = {
                                'id': worker_product_order.id,
                                'name': worker_product_order.name,
                                'product_name': worker_product_order.product_name,
                                'product_qty': worker_product_order.product_qty,
                                'finish_product': {}
                            }
                            if worker_product_order.finish_product:
                                finish_product = worker_product_order.finish_product
                                response_item['worker_product_order']['finish_product'] = {
                                    'id': finish_product.id,
                                    'order': finish_product.order.id,
                                    'work_proses': finish_product.work_proses,
                                }
                        response_item.update(company_info)
                        custom_response.append(response_item)
                return Response(custom_response, status=status.HTTP_200_OK)

            return Response({"detail": "No data found for the given STIR."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, STIR):
        try:
            company_name = CompanyName.objects.get(STIR=STIR)
        except CompanyName.DoesNotExist:
            return Response({"detail": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        for attr, value in data.items():
            setattr(company_name, attr, value)

        company_name.save()
        return Response({"detail": "Company information updated successfully."}, status=status.HTTP_200_OK)


class SoldGetView(APIView):
    def get(self, request):
        try:
            stirs = Sold.objects.values('STIR', 'company_name').annotate(total_qty=Sum('qty'))

            custom_response = []
            for stir_info in stirs:
                stir = stir_info['STIR']
                company_name = stir_info['company_name']
                total_qty = stir_info['total_qty']

                solds = Sold.objects.filter(STIR=stir, company_name=company_name)

                for sold in solds:
                    finish_product = None
                    if sold.worker_product_order.finish_product:
                        finish_product = {
                            'id': sold.worker_product_order.finish_product.id,
                            'work_proses': sold.worker_product_order.finish_product.work_proses
                        }

                    sold_item = {
                        'STIR': stir,
                        'company_name': company_name,
                        'total_qty': total_qty,
                        'sold_products': [{
                            'id': sold.id,
                            'qty': sold.qty,
                            'price': sold.price,
                            'ndc': sold.ndc,
                            'worker_product_order': {
                                'id': sold.worker_product_order.id,
                                'name': sold.worker_product_order.name,
                                'product_qty': sold.worker_product_order.product_qty,
                                'product_name': sold.worker_product_order.product_name,
                                'qty': sold.worker_product_order.qty,
                                'finish_product': finish_product
                            }
                        }]
                    }
                    custom_response.append(sold_item)

            return Response(custom_response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoldView(APIView):

    def get(self, request):
        try:
            stirs = Sold.objects.values('STIR', 'company_name').annotate(total_qty=Sum('qty'))

            custom_response = []
            for stir_info in stirs:
                stir = stir_info['STIR']
                company_name = stir_info['company_name']
                total_qty = stir_info['total_qty']

                solds = Sold.objects.filter(STIR=stir, company_name=company_name)

                sold_items = {
                    'id': stirs.id,
                    'STIR': stir,
                    'company_name': company_name,
                    'total_qty': total_qty,
                    'sold_products': []
                }

                for sold in solds:
                    sold_item = {
                        'id': sold.id,
                        'qty': sold.qty,
                        'price': sold.price,
                        'ndc': sold.ndc,
                        'worker_product_order': {
                            'id': sold.worker_product_order.id,
                            'name': sold.worker_product_order.name,
                            'product_qty': sold.worker_product_order.product_qty,
                            'product_name': sold.worker_product_order.product_name,
                            'qty': sold.worker_product_order.qty,
                            'finish_product': [
                                {
                                    'id': sold.worker_product_order.finish_product.id,
                                    'work_proses': sold.worker_product_order.finish_product.work_proses
                                }
                            ]
                        }
                    }
                    sold_items['sold_products'].append(sold_item)

                custom_response.append(sold_items)

            return Response(custom_response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = SoldSerializer(data=request.data)
        if serializer.is_valid():
            qty = serializer.validated_data.get('qty')
            price = serializer.validated_data.get('price')
            STIR = serializer.validated_data.get('STIR', '')
            company_name = serializer.validated_data.get('company_name', '')
            worker_product_order_id = serializer.validated_data['worker_product_order'].id
            print(worker_product_order_id)
            if worker_product_order_id is not None:
                try:
                    with transaction.atomic():
                        worker_product_order = WorkerProductOrder.objects.get(id=worker_product_order_id)

                        sold_instance = Sold.objects.filter(
                            worker_product_order=worker_product_order,
                            STIR=STIR,
                            company_name=company_name
                        ).first()

                        if sold_instance:
                            sold_instance.qty += qty
                            sold_instance.save()
                        else:
                            sold_instance = Sold(
                                worker_product_order=worker_product_order,
                                qty=qty,
                                price=price,
                                ndc=serializer.validated_data.get('ndc', 12),
                                STIR=STIR,
                                company_name=company_name
                            )
                            sold_instance.save()

                            sold_instance.create_company_name()

                    worker_product_order.product_qty -= qty
                    worker_product_order.save()

                    solds = Sold.objects.filter(worker_product_order=worker_product_order)

                    custom_response = [
                        {
                            'id': sold.id,
                            'qty': sold.qty,
                            'price': sold.price,
                            'ndc': sold.ndc,
                            'STIR': sold.STIR,
                            'company_name': sold.company_name,
                            'worker_product_order': {
                                'id': sold.worker_product_order.id,
                                'name': sold.worker_product_order.name,
                                'product_qty': sold.worker_product_order.product_qty,
                                'product_name': sold.worker_product_order.product_name,
                                'qty': sold.worker_product_order.qty
                            }
                        }
                        for sold in solds
                    ]
                    return Response(custom_response, status=status.HTTP_200_OK)

                except WorkerProductOrder.DoesNotExist:
                    return Response({'error': 'Worker product order not found'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response({'error': 'Worker product order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoldDetailView(APIView):
    def get(self, request, id):
        try:
            sold = Sold.objects.get(id=id)
        except Sold.DoesNotExist:
            return Response(data={'Sold not found'}, status=status.HTTP_404_NOT_FOUND)

        custom_response = {
            'id': sold.id,
            'qty': sold.qty,
            'price': sold.price,
            'ndc': sold.ndc,
            'STIR': sold.STIR,
            'company_name': sold.company_name,
            'worker_product_order': {
                'id': sold.worker_product_order.id,
                'name': sold.worker_product_order.name,
                'product_qty': sold.worker_product_order.product_qty,
                'product_name': sold.worker_product_order.product_name,
                'qty': sold.worker_product_order.qty,
                'finish_product': [
                    {
                        'id': sold.worker_product_order.finish_product.id,
                        'work_proses': sold.worker_product_order.finish_product.work_proses
                    }
                ]
            } if sold.worker_product_order else None
        }

        return Response(custom_response, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            sold = Sold.objects.get(id=id)
        except Sold.DoesNotExist:
            return Response(data={'Sold not found'}, status=status.HTTP_400_BAD_REQUEST)

        sold.delete()
        return Response(data={'Sold successfully deleted'}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            sold = Sold.objects.get(id=id)
        except Sold.DoesNotExist:
            return Response(data={'Sold not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SoldSerializer(sold, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuccessOrderView(APIView):
    def get(self, request):
        order = Order.objects.filter(status='SUCCESSFULLY')
        serializer = OrderSerializer(instance=order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FinishedProductView(APIView):
    def get(self, request):
        finish_products = FinishedProduct.objects.all()
        # finish_products_to_delete = finish_products.filter(work_proses=0)
        # finish_products_to_delete.delete()
        serializer = FinishedProductGetSerializer(instance=finish_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FinishedProductSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            work_proses = serializer.validated_data.get('work_proses')

            try:
                with transaction.atomic():
                    finished_product, created = FinishedProduct.objects.get_or_create(
                        order=order,
                        defaults={'work_proses': work_proses}
                    )
                    if not created:
                        finished_product.work_proses += work_proses
                        finished_product.save()

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinishedProductDetailView(APIView):
    def delete(self, request, id):
        try:
            finish_product = get_object_or_404(FinishedProduct, id=id)
        except:
            return Response(data={'Finish product not found'})

        finish_product.delete()
        return Response(data={'Finish product successfully deleted'})


class CompanyBalanceView(APIView):
    def get(self, request):
        company_ = CompanyBalance.objects.all()
        serializer = CompanyBalanceGetSerializer(company_, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompanyBalanceSerializer(data=request.data)
        if serializer.is_valid():
            company_id = serializer.validated_data['company'].id
            price = serializer.validated_data['price']
            company_balance_model = CompanyName.objects.get(id=company_id)
            company_balance_model.balance -= price
            company_balance_model.save()
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyBalanceDetailView(APIView):
    def get(self, request, id):
        company = get_object_or_404(CompanyBalance, id=id)
        serializer = CompanyBalanceGetSerializer(company)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        company = get_object_or_404(CompanyBalance, id=id)
        serializer = CompanyBalanceGetSerializer(company, partial=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            company = get_object_or_404(CompanyBalance, id=id)
        except:
            return Response(data='Company balance not found')

        company.delete()
        return Response(data={'Successfully deleted'})


class WorkExpenseView(APIView):
    def post(self, request):
        serializer = WorkExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyNameSoldView(APIView):
    def get(self, request):
        company_name = CompanyName.objects.exclude(sold__isnull=True)
        serializer = CompanyNameSoldSerializer(instance=company_name, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CompanyNameSoldDetailView(APIView):
    def get(self, request, id):
        try:
            company = CompanyName.objects.get(id=id)
            stirs = Sold.objects.filter(STIR=company.STIR, company_name=company.company_name).values('STIR',
                                                                                                     'company_name').annotate(
                total_qty=Sum('qty'))

            custom_response = []
            for stir_info in stirs:
                stir = stir_info['STIR']
                company_name = stir_info['company_name']
                total_qty = stir_info['total_qty']
                solds = Sold.objects.filter(STIR=stir, company_name=company_name)
                sold_products = []
                for sold in solds:
                    sold_item = {
                        'id': sold.id,
                        'qty': sold.qty,
                        'price': sold.price,
                        'ndc': sold.ndc,
                        'ndc_price': sold.ndc_price,
                        'worker_product_order': {
                            'id': sold.worker_product_order.id,
                            'name': sold.worker_product_order.name,
                            'product_qty': sold.worker_product_order.product_qty,
                            'product_name': sold.worker_product_order.product_name,
                            'qty': sold.worker_product_order.qty,
                            'finish_product': [
                                {
                                    'id': sold.worker_product_order.finish_product.id,
                                    'work_proses': sold.worker_product_order.finish_product.work_proses,
                                    'order': {
                                        'id': sold.worker_product_order.finish_product.order.id,
                                        'measurement': sold.worker_product_order.finish_product.order.measurement
                                    }
                                }
                            ]
                        }
                    }
                    sold_products.append(sold_item)
                solds_response = {
                    'id': company.id,
                    'STIR': stir,
                    'company_name': company_name,
                    'total_qty': total_qty,
                    'balance': company.balance,
                    'created_at': company.created_at,
                    'sold_products': sold_products
                }
                custom_response.append(solds_response)

            return Response(custom_response, status=status.HTTP_200_OK)

        except CompanyName.DoesNotExist:
            return Response({"detail": "Company with the specified ID does not exist."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyNameProductView(APIView):
    def get(self, request):
        company_names = CompanyName.objects.exclude(product__isnull=True)
        custom_data = [
            {
                'id': company_name.id,
                'STIR': company_name.STIR,
                'company_name': company_name.company_name,
                'balance': company_name.balance,
                'created_at': company_name.created_at,
                'products': [
                    {
                        'id': company_name.product.id,
                        'name': company_name.product.name,
                        'qty': company_name.product.qty,
                        'price': company_name.product.price,
                        'ndc_price': company_name.product.ndc_price,
                        'measurement': company_name.product.measurement,
                        'category': company_name.product.category,
                        'total_price': company_name.product.total_price,
                        'payment_price': company_name.product.payment_price,
                        'created_at': company_name.product.created_at,
                    }
                ]
            }
            for company_name in company_names
        ]
        return Response(data=custom_data, status=status.HTTP_200_OK)


class CompanyNameProductDetailView(APIView):
    def get(self, request, id):
        try:
            company_name = CompanyName.objects.exclude(product__isnull=True).get(id=id)
        except CompanyName.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        products = Enter.objects.filter(STIR=company_name.STIR)
        product_data = [
            {
                'id': product.id,
                'name': product.name,
                'qty': product.qty,
                'price': product.price,
                'ndc_price': product.ndc_price,
                'measurement': product.measurement,
                'category': product.category,
                'total_price': product.total_price,
                'payment_price': product.payment_price,
                'created_at': product.created_at,
            }
            for product in products
        ]

        custom_data = {
            'id': company_name.id,
            'STIR': company_name.STIR,
            'company_name': company_name.company_name,
            'balance': company_name.balance,
            'created_at': company_name.created_at,
            'products': product_data
        }

        return Response(custom_data, status=status.HTTP_200_OK)


class TestOrderViewSet(viewsets.ModelViewSet):
    queryset = TestOrder.objects.all()
    serializer_class = TestOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class OrderAssignmentViewSet(viewsets.ModelViewSet):
    queryset = OrderAssignment.objects.all()
    serializer_class = OrderAssignmentSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class WorkerProductOrderView(APIView):
    def get(self, request):
        worker_product_orders = WorkerProductOrder.objects.all()
        orders_dict = {}

        for order in worker_product_orders:
            key = order.name
            if key not in orders_dict:
                orders_dict[key] = {
                    'id': order.id,
                    'name': order.name,
                    'product_qty': order.product_qty,
                    'products': []
                }

            orders_dict[key]['products'].append({
                'finish_product': str(order.finish_product.id),
                'qty': order.qty,
                'product_name': order.product_name
            })

        orders_list = list(orders_dict.values())
        serializer = WorkerProductOrderDetailSerializer(orders_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkerProductOrderSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            product_qty = serializer.validated_data['product_qty']
            products = serializer.validated_data['products']

            try:
                with transaction.atomic():
                    for product in products:
                        finish_product_id = product['finish_product']
                        qty = product['qty']
                        product_name = product['product_name']

                        finish_product_model, created = FinishedProduct.objects.get_or_create(id=finish_product_id)

                        if created:
                            finish_product_model.work_proses = qty
                        else:
                            new_work_proses = finish_product_model.work_proses - qty
                            if new_work_proses < 0:
                                return Response(
                                    data={
                                        'error': f'Bu {qty} bazadagidan kop {finish_product_model.work_proses}'
                                    },
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                            finish_product_model.work_proses = new_work_proses

                        finish_product_model.save()

                        existing_order = WorkerProductOrder.objects.filter(name=name, finish_product=finish_product_model, product_name=product_name).first()

                        if existing_order:
                            existing_order.qty += qty
                            existing_order.product_qty += product_qty
                            existing_order.save()
                        else:
                            WorkerProductOrder.objects.create(
                                name=name,
                                product_qty=product_qty,
                                finish_product=finish_product_model,
                                product_name=product_name,
                                qty=qty
                            )

                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            except FinishedProduct.DoesNotExist:
                return Response(data={'error': 'Tayyor mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerProductOrderDetailView(APIView):
    def get(self, request, id):
        order = get_object_or_404(WorkerProductOrder, id=id)

        # Constructing the response dictionary
        response_data = {
            'id': order.id,
            'name': order.name,
            'product_qty': order.product_qty,
            'products': []
        }

        related_products = WorkerProductOrder.objects.filter(name=order.name, product_qty=order.product_qty)

        for product_order in related_products:
            product_data = {
                'finish_product': str(product_order.finish_product.id),
                'qty': product_order.qty,
                'product_name': product_order.product_name
            }
            response_data['products'].append(product_data)

        return Response([response_data], status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            order = get_object_or_404(WorkerProductOrder, id=id)
            related_orders = WorkerProductOrder.objects.filter(name=order.name, product_qty=order.product_qty)

            with transaction.atomic():
                for product_order in related_orders:
                    finish_product = product_order.finish_product
                    finish_product.work_proses += product_order.qty
                    finish_product.save()

                related_orders.delete()

            return Response(data={'Worker Product Order successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

        except WorkerProductOrder.DoesNotExist:
            return Response(data={'error': 'Worker Product Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
