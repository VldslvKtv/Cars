from django.shortcuts import render
import xml.etree.ElementTree as ET

TREE = ET.parse("static/parse_auto/cars.xml")
ROOT = TREE.getroot()


def get_one_elem(element):
    new_el = str(element)
    n = new_el.find(',')
    if n == -1:
        return new_el
    return new_el[:n]


def marks_and_models(tree, root):
    for child in root:
        marka = child.attrib['name']
        print(f"Марка: {marka}")
        s = tree.findall(f"mark[@name='{marka}']/")
        print(f"Модели:")
        models = []
        for elem in s:
            if elem.tag == 'folder':
                models.append(get_one_elem(elem.attrib['name']))
        print(models)


marks_and_models(TREE, ROOT)
