from django.shortcuts import render
import xml.etree.ElementTree as ET
import sqlite3 as sl

TREE = ET.parse("static/parse_auto/cars.xml")
ROOT = TREE.getroot()


def get_one_elem(element):
    new_el = str(element)
    n = new_el.find(',')
    if n == -1:
        return new_el
    return new_el[:n]


def get_marks_and_models(tree, root):
    con = sl.connect('db.sqlite3')
    cursor = con.cursor()
    for mrk in root:
        marka = mrk.attrib['name']
        cursor.execute('INSERT INTO parse_auto_marks (mark) values(?)', marka)
        print(f"Марка: {marka}")
        mdl = tree.findall(f"mark[@name='{marka}']/")
        print(f"Модели:")
        mark_id = cursor.execute('SELECT id FROM parse_auto_marks WHERE mark=?', marka)
        models = []
        for elem in mdl:
            if elem.tag == 'folder':
                cursor.execute('INSERT INTO parse_auto_models (model, fk_model_id) values(?, ?)',
                               (get_one_elem(elem.attrib['name']), int(mark_id),))
                models.append(get_one_elem(elem.attrib['name']))
        print(models)


get_marks_and_models(TREE, ROOT)
