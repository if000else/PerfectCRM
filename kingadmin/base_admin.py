



#
# sites = {
#     'crm':{
#         'customers':CustomerAdmin,
#         'customerfollowup':CustomerFollowUPAdmin,
#     }
# }

class AdminRegisterException(Exception):
    def __init__(self,msg):
        self.message = msg


class BaseAdmin(object):
    list_display = ()
    list_filter = ()
    list_per_page = 5  # display 5 items per page
    search_fields = ()
    list_editable = ()


class AdminSite(object):
    def __init__(self):
        self.registered_sites = {}

    def register(self,model,admin_class=None):
        app_name = model._meta.app_label
        model_name = model._meta.model_name

        if app_name not in self.registered_sites:
            self.registered_sites[app_name] = {}


        if model_name in self.registered_sites[app_name]:
            raise AdminRegisterException("app [%s] model [%s] has already registered!" %(app_name,model_name))

        if not admin_class:
            #use baseadmin
            admin_class = BaseAdmin
        admin_obj = admin_class()
        admin_obj.model = model

        self.registered_sites[app_name][model_name] = admin_obj



site = AdminSite()
