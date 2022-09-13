from django.contrib import admin
from . models import vendor,deal_payment,BillPlan,vendor_bill_plan,free_plan_expired,agent_info


admin.site.register(vendor)
admin.site.register(BillPlan)
admin.site.register(vendor_bill_plan)
admin.site.register(free_plan_expired)
admin.site.register(agent_info)
admin.site.register(deal_payment)
