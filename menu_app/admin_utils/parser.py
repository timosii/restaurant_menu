import openpyxl


def form_data() -> dict:
    book = openpyxl.open('admin/Menu.xlsx', read_only=True, data_only=True)
    sheet = book.active
    rows = []

    for row in sheet.iter_rows(values_only=True):
        if any(cell is not None for cell in row):
            rows.append(row)

    menu_list = []
    submenu_list = []
    dish_list = []
    menus_counter = -1
    submenus_counter = -1
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if j == 0 and all([rows[i][j], rows[i][j + 1], rows[i][j + 2]]):
                menus_counter += 1
                menu_list.append({'id': f'{rows[i][j]}',
                                  'title': f'{rows[i][j + 1]}',
                                  'description': f'{rows[i][j + 2]}'})

            if j == 1 and all([rows[i][j], rows[i][j + 1], rows[i][j + 2]]):
                submenus_counter += 1
                submenu_list.append({'id': f'{rows[i][j]}',
                                     'title': f'{rows[i][j + 1]}',
                                     'description': f'{rows[i][j + 2]}',
                                     'parent_menu_id': menu_list[menus_counter]['id']})
            if j == 2 and all([rows[i][j], rows[i][j + 1], rows[i][j + 2]]):
                dish_list.append(
                    {'id': f'{rows[i][j]}',
                     'title': f'{rows[i][j + 1]}',
                     'description': f'{rows[i][j + 2]}',
                     'price': rows[i][j + 3],
                     'parent_menu_id': menu_list[menus_counter]['id'],
                     'parent_submenu_id': submenu_list[submenus_counter]['id'],
                     'discount': rows[i][j + 4]})

    return {'menus': menu_list, 'submenus': submenu_list, 'dishes': dish_list}
