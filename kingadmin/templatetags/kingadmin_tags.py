from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta

register = template.Library()


@register.simple_tag
def get_model_verbose_name(model_obj):
    model_name = model_obj._meta.verbose_name if model_obj._meta.verbose_name else model_obj._meta.verbose_name_plural

    if not model_name:
        model_name = model_obj._meta.model_name

    print("model obj", model_obj)
    return model_name.capitalize()


@register.simple_tag
def get_model_name(model_obj):
    return model_obj._meta.model_name


@register.simple_tag
def get_app_name(model_obj):
    return model_obj._meta.app_label


@register.simple_tag
def build_table_row(admin_obj, obj):
    row_ele = ""

    for column in admin_obj.list_display:
        column_obj = obj._meta.get_field(column)
        if column_obj.choices:
            get_column_data = getattr(obj, "get_%s_display" % column)
            column_data = get_column_data()
        else:
            column_data = getattr(obj, column)
        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime('%Y-%m-%d %H:%M:%S')

        td_ele = '''<td>%s</td>''' % column_data
        row_ele += td_ele

    return mark_safe(row_ele)


@register.simple_tag
def get_filter_field(filter_column, admin_obj):
    # print("admin obj",admin_obj.model ,filter_column)
    # 获取数据库中的字段对象，用来获取choices
    field_obj = admin_obj.model._meta.get_field(filter_column)
    select_ele = """<select name="%s"> """  # 记得format 回来
    selected = admin_obj.filter_conditions.get(filter_column, 'no_field')
    date_select = admin_obj.filter_conditions.get('%s__gte' % filter_column)
    # 有可能没有choices
    try:
        choices = field_obj.get_choices()
    except AttributeError as e:
        print('reflect field error [%s]' % field_obj, e)
    else:
        for choice in choices:
            if selected == str(choice[0]):
                select_option = '<option value=%s selected>%s</option>' % (choice[0], choice[1])
            else:
                select_option = '<option value=%s>%s</option>' % (choice[0], choice[1])
            select_ele += select_option
    if type(field_obj).__name__ in ('DateTimeField', 'DateField'):
        date_ele = []
        today_elt = datetime.now().date()
        date_ele.append(['所有时间', ''])
        date_ele.append(['今天', today_elt])
        date_ele.append(['昨天', today_elt - timedelta(days=1)])
        date_ele.append(['近七天', today_elt - timedelta(days=7)])
        date_ele.append(['本月', today_elt.replace(day=1)])
        date_ele.append(['近三十天', today_elt - timedelta(days=30)])
        for item in date_ele:
            # print(str(item[1]))
            if date_select == str(item[1]):
                selected = 'selected'
            else:
                selected = ''
            select_option = '<option value=%s %s>%s</option>' % (item[1], selected, item[0])
            select_ele += select_option
        # format
        select_ele %= '%s__gte' % filter_column
    else:
        select_ele = select_ele % filter_column

    select_ele += '</select>'
    return mark_safe(select_ele)


@register.simple_tag
def get_orderby_key(request, colomn):
    order_key = request.GET.get('o')
    if order_key == colomn:  # 当前列有排序
        if order_key.startswith('-'):
            return order_key.strip('-')
        else:
            return '-%s' % colomn
    return colomn


@register.simple_tag
def generate_filter_url(request, admin_obj):
    q = request.GET.get('q')
    url = ''
    if admin_obj.filter_conditions:
        for k, v in admin_obj.filter_conditions.items():
            url += "%s=%s" % (k, v)
    if q:
        url += "&q=%s" % q
    return url


@register.simple_tag
def display_order_by_icon(request, column):
    order_field = request.GET.get('o')
    if order_field:  # 查找到被排序的列
        if order_field.strip('-') == column:  # 当前列被排序
            # print('当前列被排序列：', column)
            if order_field.startswith('-'):
                icon = 'bottom'
            else:
                icon = 'top'
            ele = """<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>""" % icon

            return mark_safe(ele)
    return ''


@register.filter
def get_search_field(request):
    '''
    return the field value of 'q' to frontier
    :param request:
    :return:
    '''
    field = request.GET.get('q')
    return field


@register.simple_tag
def generate_paginator(request, page_info, admin_obj):
    '''
    生成分页器显示
    '''
    q = request.GET.get('q', '')
    o = request.GET.get('o', '')
    condition = ''
    if admin_obj.filter_conditions:
        for k, v in admin_obj.filter_conditions.items():
            condition += "%s=%s&" % (k, v)
    condition += 'q=%s&' % q
    condition += 'o=%s&' % o

    length = page_info['length']  # int
    last = page_info['last']  # int #最后一个页面
    current = page_info['current']  # int 当前页面
    num_container = int(last / length)  # 要用给多少容器
    position = int(current / length)  # 第几个容器
    if last % length:  # 最后一排有余数
        num_container += 1
    if current % length:  # 要多拿一个容器
        position += 1
    start = (position - 1) * length + 1
    if last:  # 有数据
        ele = ''
        # 有上一排
        if position > 1:
            ele += '''<li class=""><a href="?%spage=%s" aria-label="Previous">
            <span aria_hidden="true">&laquo;</span></a></li>''' % (condition, start - 1)
        # 写数据
        range_flag = start + length
        if start + 5 > last:
            range_flag = last + 1  # 要取到最后一个
        tmp = start
        while tmp < range_flag:
            if current == tmp:
                ele += '''<li class="active"><a href="?%spage=%s">%s</a> </li>''' % (condition, tmp, tmp)
            else:
                ele += '''<li><a href="?%spage=%s">%s</a> </li>''' % (condition, tmp, tmp)
            tmp += 1
        if position < num_container:
            ele += '''<li class=""><a href="?%spage=%s" aria-label="Previous">
            <span aria_hidden="true">&raquo;</span></a></li>''' % (condition, start + 5)

        return mark_safe(ele)
    return ''
