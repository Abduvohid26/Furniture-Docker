from django.urls import path, include
from .views import Product, ProductDetail, OrderAPIView, OrderDetailAPIView, \
    WorkerProductAPIView, WorkerProductDetailAPIView, AllSendMessageView, \
    MessageSendAPIView, MessageSendDetailAPIView, SendMessageView, weekly_order_stats, \
    Worker_Orders, WorkerWorkAPIView, \
    Worker_Orders_Delete, FilterDateAIView, CostAPIView, CostDetailAPIView, \
    CompanyProductAPIView, CompanyProductDetailAPIView, WorkerProductGetAPIView, NoActiveOrder, \
    FilterDateCostView, WorkerProductAllGetAPIView, ProductFilterDateAIView, CompanyNameView, \
    SoldView, SuccessOrderView, FilterSoldDateAIView, FinishedProductView, \
    SoldDetailView, CompanyBalanceView, CompanyNameGetView, FilterSoldSTIRDateAIView, CompanyBalanceDateFilter, \
    WorkStaticsFilterDateAPIView, WorkExpenseView, CompanyNameProductView, CompanyNameSoldView, \
    CompanyNameSoldDetailView, CompanyNameProductDetailView, WorkerProductAdminSendView, \
    WorkerProductAdminDetailSendView, WorkerProductNoConfirmedView, WorkerProductRejectView, TestOrderViewSet, \
    OrderAssignmentViewSet, WorkerProductOrderView, WorkerProductOrderDetailView, FinishedProductDetailView, \
    CompanyBalanceDetailView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'test-orders', TestOrderViewSet, basename='test-order')
router.register(r'order-assignments', OrderAssignmentViewSet, basename='order-assignment')
app_name = 'core'

urlpatterns = [
    path('api/', Product.as_view()),
    path('api/<uuid:id>/', ProductDetail.as_view()),
    path('order/api/', OrderAPIView.as_view()),
    path('order/api/<uuid:id>/', OrderDetailAPIView.as_view()),
    path('worker-product/api/', WorkerProductAPIView.as_view()),
    path('worker-product/api/<uuid:id>/', WorkerProductDetailAPIView.as_view()),
    path('worker-product/admin-send/', WorkerProductAdminSendView.as_view()),
    path('worker-product/admin-send/<uuid:pk>/', WorkerProductAdminDetailSendView.as_view()),
    path('worker-product/no-confirmed/<uuid:worker_id>/', WorkerProductNoConfirmedView.as_view()),
    path('worker-product/reject/<uuid:worker_id>/', WorkerProductRejectView.as_view()),
    path('message/api/', SendMessageView.as_view()),
    path('all_message/api/', AllSendMessageView.as_view()),
    path('message_send/api/', MessageSendAPIView.as_view()),
    path('message_send/api/<uuid:id>/', MessageSendDetailAPIView.as_view()),
    path('order_status/api/weekly/', weekly_order_stats),
    path('worker-orders/<uuid:worker_id>/', Worker_Orders.as_view()),
    path('worker-work/<uuid:worker_id>/', WorkerWorkAPIView.as_view()),
    path('worker-work-delete/<uuid:id>/', Worker_Orders_Delete.as_view()),
    path('filter-date/', ProductFilterDateAIView.as_view()),
    path('order/filter-date/', FilterDateAIView.as_view()),
    path('sold/filter-date/', FilterSoldDateAIView.as_view()),
    path('expense/filter-date/', FilterDateCostView.as_view()),
    path('company-filter-date/<str:STIR>/', FilterSoldSTIRDateAIView.as_view()),
    path('company-balance-filter-date/', CompanyBalanceDateFilter.as_view()),
    path('worker-static-filter-date/', WorkStaticsFilterDateAPIView.as_view()),
    path('expense/', CostAPIView.as_view()),
    path('expense/<uuid:pk>/', CostDetailAPIView.as_view()),
    path('company-product/', CompanyProductAPIView.as_view()),
    path('company-product/<uuid:pk>/', CompanyProductDetailAPIView.as_view()),
    path('worker-product-get/<uuid:worker_id>/', WorkerProductGetAPIView.as_view()),
    path('worker-product-get/', WorkerProductAllGetAPIView.as_view()),
    path('no-active-order/', NoActiveOrder.as_view()),
    path('company-name/<str:STIR>/', CompanyNameView.as_view()),
    path('company-name/', CompanyNameGetView.as_view()),
    path('sold/<uuid:id>/', SoldDetailView.as_view()),
    path('sold/', SoldView.as_view()),
    path('success-order/', SuccessOrderView.as_view()),
    path('finish-product/', FinishedProductView.as_view()),
    path('finish-product/<uuid:id>/', FinishedProductDetailView.as_view()),
    path('company-balance/', CompanyBalanceView.as_view()),
    path('company-balance/<uuid:id>/', CompanyBalanceDetailView.as_view()),
    path('worker-expense/', WorkExpenseView.as_view()),
    path('company-name-product/', CompanyNameProductView.as_view()),
    path('company-name-product/<uuid:id>/', CompanyNameProductDetailView.as_view()),
    path('company-name-sold/', CompanyNameSoldView.as_view()),
    path('company-name-sold/<uuid:id>/', CompanyNameSoldDetailView.as_view()),
    path('worker-product-order/', WorkerProductOrderView.as_view()),
    path('worker-product-order/<int:id>/', WorkerProductOrderDetailView.as_view()),
    path('salom/qale', include(router.urls)),
]
