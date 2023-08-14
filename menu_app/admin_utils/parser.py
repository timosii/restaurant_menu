import openpyxl


def parse_menu():
    book = openpyxl.open('admin/Menu.xlsx', read_only=True, data_only=True)
    sheet = book.active
    rows = []

    for row in sheet.iter_rows(values_only=True):
        if any(cell is not None for cell in row):
            rows.append(row)

    menus = []
    menus_counter = -1
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if j == 0 and all([rows[i][j], rows[i][j + 1], rows[i][j + 2]]):
                menus_counter += 1
                menus.append({'id': f'{rows[i][j]}',
                              'title': f'{rows[i][j + 1]}',
                              'description': f'{rows[i][j + 2]}',
                              'submenus': []})
                submenus_counter = -1
            if j == 1 and all([rows[i][j], rows[i][j + 1], rows[i][j + 2]]):
                submenus_counter += 1
                menus[menus_counter]['submenus'].append({'id': f'{rows[i][j]}',
                                                         'title': f'{rows[i][j + 1]}',
                                                         'description': f'{rows[i][j + 2]}',
                                                         'parent_menu_id': menus[menus_counter]['id'],
                                                         'dishes': []})
            if j == 2 and all([rows[i][j], rows[i][j + 1], rows[i][j + 2]]):
                menus[menus_counter]['submenus'][submenus_counter]['dishes'].append(
                    {'id': f'{rows[i][j]}',
                     'title': f'{rows[i][j + 1]}',
                     'description': f'{rows[i][j + 2]}',
                     'price': f'{rows[i][j + 3]}',
                     'parent_menu_id': menus[menus_counter]['id'],
                     'parent_submenu_id': menus[menus_counter]['submenus'][submenus_counter]['id']})

    return menus


def form_chunks():
    menus = parse_menu()
    menu_list = []
    submenu_list = []
    dish_list = []

    for menu in menus:
        menu_list.append({
            'id': menu['id'],
            'title': menu['title'],
            'description': menu['description']
        })
        for submenu in menu['submenus']:
            submenu_list.append({
                'id': submenu['id'],
                'title': submenu['title'],
                'description': submenu['description'],
                'parent_menu_id': submenu['parent_menu_id']
            })
            for dish in submenu['dishes']:
                dish_list.append({
                    'id': dish['id'],
                    'title': dish['title'],
                    'description': dish['description'],
                    'price': dish['price'],
                    'parent_menu_id': dish['parent_menu_id'],
                    'parent_submenu_id': dish['parent_submenu_id']
                })

    return {'menus': menu_list, 'submenus': submenu_list, 'dishes': dish_list}
