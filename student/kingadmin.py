from kingadmin.base_admin import site,BaseAdmin
from student import models

class TestModelAdmin(BaseAdmin):
    list_display = ('name','mobile')
    search_fields = ('name',)
    list_filter = ('name','mobile')
site.register(models.TestModel,TestModelAdmin)