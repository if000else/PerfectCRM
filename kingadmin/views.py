from django.shortcuts import render
from django.db.models import Q
from django import conf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# print("dj conf:",conf.settings)


from crm.kingadmin import *
# from student.kingadmin import *
from kingadmin import base_admin


def app_index(request, ):
    # for app in conf.settings.INSTALLED_APPS:
    #     print(app)
    print("registered_sites", base_admin.site.registered_sites)
    registered_sites = base_admin.site.registered_sites
    return render(request, 'kingadmin/app_index.html',
                  {"registered_sites": registered_sites})


def app_detail(request, app_name):
    # for app in conf.settings.INSTALLED_APPS:
    #     print(app)
    print("registered_sites", base_admin.site.registered_sites)
    registered_sites = base_admin.site.registered_sites
    return render(request, 'kingadmin/app_index.html',
                  {'registered_sites': {app_name: registered_sites[app_name]}})


def table_data_list(request, app_name, model_name):
    # 获取模板设置
    admin_obj = base_admin.site.registered_sites[app_name][model_name]
    # 获取所有数据
    objs = admin_obj.model.objects.all()

    # filter data
    querysets, conditions = filter_querysets(request, objs)

    # faintly query
    faint_querysets = faint_query(request, querysets, admin_obj)

    # order
    order_queryset = get_order_querysets(request, faint_querysets)

    # pagenate
    paginator = Paginator(order_queryset, admin_obj.list_per_page)
    page = request.GET.get('page', 1)
    if int(page) > paginator.num_pages:
        page = paginator.num_pages
    page_info = {}
    length = 5  # 每排显示多少页
    page_info['length'] = length
    page_info['current'] = int(page)  # 当前页面
    page_info['last'] = int(paginator.num_pages)  # 最后一个页面
    try:
        page_objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_objs = paginator.page(paginator.num_pages)

    admin_obj.querysets = page_objs
    admin_obj.filter_conditions = conditions

    return render(request, "kingadmin/table_data_list.html", locals())


def filter_querysets(request, queryset):
    conditions = {}
    # print(request.GET)
    # 过滤关键字
    for k, v in request.GET.items():
        if k in ("page", "o", "q",'date'):
            continue
        if v:
            conditions[k] = v

    query_res = queryset.filter(**conditions)
    print("filter condtions:", conditions)
    return query_res, conditions


def get_order_querysets(request, querysets):
    order_field = request.GET.get('o')
    if order_field:
        res_querysets = querysets.order_by(order_field)
        print("order by:", order_field)
    else:
        res_querysets = querysets.order_by('id')
        print('order by:id')
    return res_querysets


def faint_query(request, querysets, admin_obj):
    search_key = request.GET.get('q')
    q = Q()
    q.connector = 'OR'
    if search_key:
        for key in admin_obj.search_fields:
            q_condition = "%s__contains" % (key)
            q.children.append((q_condition, search_key))
    return querysets.filter(q)
