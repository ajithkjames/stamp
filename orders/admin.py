from django.contrib import admin

from .models import *

class OrderDetailAdmin(admin.ModelAdmin):
	list_display=('stamp_type','user',)
	search_fields = ('stamp_type','user__first_name','user__email')
admin.site.register(Profile)
admin.site.register(OrderDetail,OrderDetailAdmin)