from django.shortcuts import render
import xml.etree.ElementTree as Et
import sqlite3 as sl
from parse_auto import models as md
from parse_auto.car_data import parse_file, create_massiv_models


def delete_data():
    con = sl.connect("D:/Projects/cars/cars/db.sqlite3")
    cursor = con.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute('DELETE FROM parse_auto_marks')
    cursor.execute('DELETE FROM parse_auto_models')
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=?", (0,))
    con.commit()
    con.close()


def get_data():
    tree = Et.parse("parse_auto/static/parse_auto/cars.xml")
    dict_auto = parse_file(tree)
    for mrk, mdl in dict_auto.items():
        try:
            new_mark = md.Marks.objects.get_or_create(mark=mrk)[0]
            mark_identi = new_mark.pk
            mas_models = create_massiv_models(mdl, mark_identi)
            md.Models.objects.bulk_create(mas_models)
        except:
            pass
    marks = md.Marks.objects.all()
    return marks


def get_marks(request):
    delete_data()
    all_marks = get_data()
    return render(request, 'parse_auto/update_autoru_catalog.html', {'all_marks': all_marks})


def get_models(request):
    if request.method == 'POST':
        brand_pk = request.POST['brand']
        all_marks = md.Marks.objects.all()
        fk_models = md.Models.objects.filter(fk_model=brand_pk)
        return render(request, 'parse_auto/update_autoru_catalog.html', {'fk_models': fk_models,
                                                                         'all_marks': all_marks})