from django.db import IntegrityError
from django.shortcuts import render
import xml.etree.ElementTree as ET
import sqlite3 as sl
from parse_auto import models as md


# TREE = ET.parse("parse_auto/static/parse_auto/cars.xml")
# ROOT = TREE.getroot()


def get_one_elem(element):
    new_el = str(element)
    n = new_el.find(',')
    if n == -1:
        return new_el
    return new_el[:n]


def parse_file(tree):
    root = tree.getroot()
    auto = {}
    for mrk in root:
        marka = mrk.attrib['name']
        mdl = tree.findall(f"mark[@name='{marka}']/")
        models_all = set()
        for elem in mdl:
            if elem.tag == 'folder':
                models_all.add(get_one_elem(elem.attrib['name']))
        auto[marka] = list(models_all)
    return auto


def create_massiv_models(mas, mark):
    new_mas = []
    for elem in mas:
        new_mas.append(md.Models(model=elem, fk_model=md.Marks.objects.get(pk=int(mark))))
    return new_mas


def delete_data():
    con = sl.connect("D:/Projects/cars/cars/db.sqlite3")
    cursor = con.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute('DELETE FROM parse_auto_marks')
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=?", (0,))
    cursor.execute('DELETE FROM parse_auto_models')
    con.commit()
    con.close()


def get_marks_and_models(request):
    delete_data()
    tree = ET.parse("parse_auto/static/parse_auto/cars.xml")
    dict_auto = parse_file(tree)
    for mrk, mdl in dict_auto.items():
        new_mark = md.Marks(mark=mrk)
        new_mark.save()
        mark_identi = new_mark.pk
        mas_models = create_massiv_models(mdl, mark_identi)
        md.Models.objects.bulk_create(mas_models)
    return render(request, 'parse_auto/home.html')


# def get_marks_and_models(request):
#     delete_data()
#     tree = ET.parse("parse_auto/static/parse_auto/cars.xml")
#     dict_auto = parse_file(tree)
#     root = tree.getroot()
#     # con = sl.connect("D:/Projects/cars/cars/db.sqlite3")
#     # cursor = con.cursor()
#     for mrk in root:
#         marka = mrk.attrib['name']
#         # cursor.execute('INSERT INTO parse_auto_marks (mark) values(?)', (marka,))
#         new_mark = md.Marks(mark=marka)
#         new_mark.save()
#         # print(f"Марка: {marka}")
#         mdl = tree.findall(f"mark[@name='{marka}']/")
#         # print(f"Модели:")
#         # cursor.execute('SELECT id FROM parse_auto_marks WHERE mark=?', (marka,))
#         # mark_id = cursor.fetchall()[0][0]
#         mark_id = new_mark.pk
#         # models_all = []
#         for elem in mdl:
#             if elem.tag == 'folder':
#                 try:
#                     new_model = md.Models(model=get_one_elem(elem.attrib['name']),
#                                           fk_model=md.Marks.objects.get(pk=int(mark_id)))
#                     new_model.save()
#                 except IntegrityError:
#                     pass
#                 # cursor.execute('INSERT INTO parse_auto_models (model, fk_model_id) values(?, ?)',
#                 # (get_one_elem(elem.attrib['name']), int(mark_id),))
#                 # models_all.append(get_one_elem(elem.attrib['name']))
#         # print(models_all)
#     return render(request, 'parse_auto/home.html')
#     # con.commit()
#     # con.close()

