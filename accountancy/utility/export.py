from accountancy.models import Class, Note, Group
from django.db.models import F, Sum
from accountancy.constants import FileLabels

def export_file(f_id):
    """
    формирует структуру данных для отображения на шаблоне, выполняя запросы в бд.
    """
    export_list = []
    classes = Class.objects.filter(note__file_id__exact=f_id).values_list('id',
                                                                          flat=True).distinct().order_by('id')
    for c in classes:
        groups = Group.objects.filter(note__file_id__exact=f_id,
                                      note__class_id__exact=c).values_list('id',
                                                                           flat=True).distinct().order_by('id')
        temp_list = [Class.objects.get(id=c).name]
        export_list.append(temp_list)
        for g in groups:
            q = q_append_outcoming_fields(q_filter(f_id, c, g))
            for i in q_values(q):
                i = list(i)
                i[0] = format_code(i, q)
                export_list.append(i)  # добавляем строку с 4-ёх значным числом
            l = list(q_sum(q))
            l.insert(0, q[0].group_id.code)
            export_list.append(l)  # добавляем строку с двузначным числом (по группе)
        q = q_append_outcoming_fields(q_filter(f_id,c))
        l = list(q_sum(q))
        l.insert(0, FileLabels.ABOUT_CLASS)  # добавляем строку с "ПО КЛАССУ"
        export_list.append(l)
    q = q_append_outcoming_fields(q_filter(f_id))
    l = list(q_sum(q))
    l.insert(0, FileLabels.BALANCE)
    export_list.append(l)  # добавляем строку с "БАЛАНС"
    # print(export_list)
    return export_list


def q_values(q):
    return q.values_list(
        'code', 'incoming_liability', 'incoming_asset', 'debit', 'credit', 'outcoming_liability',
        'outcoming_asset').order_by('id')


def q_sum(q):
    return q.aggregate(Sum('incoming_liability'),
                       Sum('incoming_asset'), Sum('debit'),
                       Sum('credit'),
                       Sum('outcoming_liability'),
                       Sum('outcoming_asset')).values()


def q_append_outcoming_fields(q):
    """
    добавляет к запросы вычисляемые поля, тут можно задать любую формулу
    """
    return q.annotate(
        outcoming_liability=F('incoming_liability') - F('incoming_asset') + F('debit') - F('credit'),
        outcoming_asset=-F('incoming_liability') + F('incoming_asset') - F('debit') + F('credit'))


def q_filter(f_id, c_id=0, g_id=0):
    """
    выбирает записи, используя те значения фильтра, которые даны
    """
    if g_id == 0 and c_id == 0:
        q = Note.objects.filter(file_id=f_id)
    elif g_id == 0:
        q = Note.objects.filter(file_id=f_id, class_id=c_id)
    else:
        q = Note.objects.filter(file_id=f_id, class_id=c_id, group_id=g_id)
    return q


def format_code(i, q):
    """
    код группы это 01, а не 1
    """
    if i[0] < 10:
        i[0] = '0' + str(i[0])
    return str(q[0].group_id.code) + str(i[0])
