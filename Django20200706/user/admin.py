from user.models import User, Address
from django.contrib import admin


# Register your models here.

# class MyAdminSite(admin.AdminSite):
#     site_header = '未来鲜生'
#     site_title = '未来鲜生'
#
# admin_site = MyAdminSite(name='management')

class UserAdmin(admin.ModelAdmin):
    #设置用户显示
    list_display = ['username','phone','first_name','last_name','date_joined']
    #设置每页的记录数  默认100条
    list_per_page = 10
    #排序
    ordering = ['date_joined']
    #设置默认可编辑字段
    list_editable = ['phone']
    #过滤查询
    list_filter = ['username','phone','first_name']
    #搜索查询
    search_fields = ['username']
    #日期的登记划分
    date_hierarchy = 'date_joined'

class AddressAdmin(admin.ModelAdmin):
    #设置用户显示
    list_display = ['recevier','addr','phone','add_time','user']

admin.site.register(User,UserAdmin)
admin.site.register(Address,AddressAdmin)

admin.site.site_header = '未来鲜生后台管理'
admin.site.site_title = '未来鲜生'

# admin_site.register(User,UserAdmin)
