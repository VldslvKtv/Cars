from parse_auto import models as md


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
