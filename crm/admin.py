from django.contrib import admin

# Register your models here.
from crm import models


class CustomerAdmin(admin.ModelAdmin):
    # 显示列名称
    list_display = ('id','qq', 'name', 'consultant','consult_course', 'content', 'source', 'date')
    # 过滤字段
    list_filter = ('source', 'consultant', 'date')
    # 搜索条件，关系是或
    search_fields = ('qq', 'name',)
    #
    # raw_id_fields = ('consult_course',)
    # 水平过滤
    # filter_horizontal = ('tags',)
    # 可编辑
    list_editable = ('source',)

admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Branach)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.CourseRecord)
admin.site.register(models.CustomerFollowUP)
admin.site.register(models.Enrollment)
admin.site.register(models.Payment)
admin.site.register(models.Role)
admin.site.register(models.StudyRecord)
admin.site.register(models.Tag)
admin.site.register(models.UserProfile)
admin.site.register(models.Menu)
