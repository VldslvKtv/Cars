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


def is_empty():
    con = sl.connect("D:/Projects/cars/cars/db.sqlite3")
    cursor = con.cursor()
    db_content = cursor.execute("SELECT COUNT(*) FROM parse_auto_marks")
    rows = db_content.fetchall()
    con.close()
    if rows:
        return True
    return False


def get_marks(request):
    if is_empty():
        delete_data()
        tree = Et.parse("parse_auto/static/parse_auto/cars.xml")
        dict_auto = parse_file(tree)
        for mrk, mdl in dict_auto.items():
            new_mark = md.Marks(mark=mrk)
            new_mark.save()
            mark_identi = new_mark.pk
            mas_models = create_massiv_models(mdl, mark_identi)
            md.Models.objects.bulk_create(mas_models)
        all_marks = md.Marks.objects.all()
        return render(request, 'parse_auto/update_autoru_catalog.html', {'all_marks': all_marks})
    all_marks = md.Marks.objects.all()
    return render(request, 'parse_auto/update_autoru_catalog.html', {'all_marks': all_marks})


def get_models(request):
    if request.method == 'POST':
        brand_pk = request.POST['brand']
        all_marks = md.Marks.objects.all()
        all_models = md.Models.objects.filter(fk_model=brand_pk)
        return render(request, 'parse_auto/catalog.html', {'all_models': all_models,
                                                           'all_marks': all_marks})
