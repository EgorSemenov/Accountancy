from accountancy.models import Class, Note, Group
from django.db.models import F, Sum


def export_file(f_id):
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
            q = q_annotate(f_id, c, g)
            for i in list(q_values(q)):
                i = list(i)
                if i[0] < 10:
                    i[0] = '0' + str(i[0])
                i[0] = str(q[0].group_id.code) + str(i[0])
                export_list.append(i)
            l = list(q_aggregate(q))
            l.insert(0, q[0].group_id.code)
            export_list.append(l)
        q = q_annotate(f_id, c)
        l = list(q_aggregate(q))
        l.insert(0, 'ПО КЛАССУ')
        export_list.append(l)
    q = q_annotate(f_id)
    l = list(q_aggregate(q))
    l.insert(0, 'БАЛАНС')
    export_list.append(l)
    # print(export_list)
    return export_list


def q_values(q):
    return q.values_list(
        'code', 'incoming_liability', 'incoming_asset', 'debit', 'credit', 'outcoming_liability',
        'outcoming_asset').order_by('id')


def q_aggregate(q):
    return q.aggregate(Sum('incoming_liability'),
                       Sum('incoming_asset'), Sum('debit'),
                       Sum('credit'),
                       Sum('outcoming_liability'),
                       Sum('outcoming_asset')).values()


def q_annotate(f_id, c_id=0, g_id=0):
    if g_id == 0 and c_id == 0:
        q = Note.objects.filter(file_id=f_id)
    elif g_id == 0:
        q = Note.objects.filter(file_id=f_id, class_id=c_id)
    else:
        q = Note.objects.filter(file_id=f_id, class_id=c_id, group_id=g_id)
    query = q.annotate(
        outcoming_liability=F('incoming_liability') - F('incoming_asset') + F('debit') - F('credit'),
        outcoming_asset=-F('incoming_liability') + F('incoming_asset') - F('debit') + F('credit'))
    return query
