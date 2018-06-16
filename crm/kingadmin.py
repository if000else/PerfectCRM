
from kingadmin.base_admin import site,BaseAdmin
from crm import models

print("kingadmin setting enable...")
class CustomerAdmin(BaseAdmin):
    list_display = ('id', 'name', 'qq','status', 'consultant', 'source', 'memo', 'date')
    list_filter = ('source', 'consultant','status')
    search_fields = ('qq', 'name',)
    list_editable = ('source',)
    list_per_page = 2
    # readonly_fields = ('name',)
    # actions = ["change_status", ]
    def change_status(self,request,querysets):
        print("changeing status",querysets)
        querysets.update(status=1)

    change_status.short_description = "改变报名状态"
class ClassListAdmin(BaseAdmin):
    list_display = ('id','course','semester',)

site.register(models.Customer,CustomerAdmin)
site.register(models.ClassList,ClassListAdmin)
# site.register(models.CourseRecord)