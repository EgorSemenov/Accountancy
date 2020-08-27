from django.db import models


# Create your models here.
class File(models.Model):  # класс-сущность таблицы файл
    id = models.IntegerField('id файла', primary_key=True)
    name = models.CharField('имя файла', max_length=255)


class Class(models.Model):  # класс-сущность таблицы класс
    id = models.IntegerField('id класса', primary_key=True)
    name = models.CharField('имя класса', max_length=255)


class Group(models.Model):  # класс-сущность таблицы группа
    id = models.IntegerField('id группы', primary_key=True)
    code = models.IntegerField('номер группы')


class Note(models.Model):   # класс-сущность таблицы запись
    id = models.IntegerField('id записи', primary_key=True)
    code = models.IntegerField('номер записи')
    incoming_liability = models.FloatField('входящий пассив')
    incoming_asset = models.FloatField('входящий актив')
    debit = models.FloatField('обороты-дебет')
    credit = models.FloatField('обороты-кредит')
    # outcoming_liability = models.FloatField('исходящий пассив')  это поле высчитывается
    # outcoming_asset = models.FloatField('исходящий актив')        это поле высчитывается
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
