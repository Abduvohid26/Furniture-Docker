from django.contrib import admin
from .models import Enter, Order, WorkerProduct, Message, WorkerProductGet, WorkerWork, \
    CompanyName, Sold, CompanyProduct, FinishedProduct, Expense, CompanyBalance, WorkerExpense, WorkerProductSendAdmin, \
    OrderAssignment, TestOrder, WorkerProductOrder
# Register your models here.
# from django.contrib.auth import get_user_model
# User = get_user_model()
from users.models import User


class WorkerProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "worker":
            kwargs["queryset"] = User.objects.filter(user_roles='worker')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MessageAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "worker":
            kwargs["queryset"] = User.objects.filter(user_roles='worker')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Message, MessageAdmin)
admin.site.register(WorkerProduct, WorkerProductAdmin)
admin.site.register(Enter)
admin.site.register(Order)
admin.site.register(WorkerProductGet)
admin.site.register(WorkerWork)
admin.site.register(CompanyName)
admin.site.register(Sold)
admin.site.register(CompanyProduct)
admin.site.register(FinishedProduct)
admin.site.register(Expense)
admin.site.register(CompanyBalance)
admin.site.register(WorkerExpense)
admin.site.register(WorkerProductSendAdmin)
admin.site.register(OrderAssignment)
admin.site.register(TestOrder)
admin.site.register(WorkerProductOrder)
