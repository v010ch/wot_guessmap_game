''''''
#!/usr/bin/env python
# coding: utf-8
import os
import json


def collect_map_names(inp_path: str) -> tuple[list, dict, dict]:
    '''
    '''
    all_map_names = []
    maps_numb = dict()
    ru_map_names = dict()

    all_files = os.listdir(inp_path)
    used_numbs = set()
    for filename in all_files:
        numb = filename.split('_')[0]
        try:
            numb = int(numb)
        except:
            continue
        if not numb in used_numbs:
            map_name = '_'.join(filename.split('.')[0]\
                                        .split('_')[1:]
                               )
            all_map_names.append(map_name)
            maps_numb[map_name] = numb
            ru_map_names[map_name] = 'неизвестно'
            used_numbs.add(numb)

    #print(all_map_names)
    return all_map_names, maps_numb, ru_map_names


def create_map_info_json(path_to_wot_res_packages: str) -> None:
    '''
    '''
    if not os.path.exists(path_to_wot_res_packages):
        print('Wrong path to wot res packages. Retire!')
        return -1

    all_map_names, maps_numb, ru_map_names = collect_map_names(path_to_wot_res_packages)

    # Сохраняю как json
    maps_json = {'all_map_names': all_map_names,
                 'maps_numb': maps_numb,
                 'ru_map_names': ru_map_names,
                }
    json_filename = 'maps_info.json'
    with open(os.path.join('.', 'data', json_filename), 'w') as fd:
        json.dump(maps_json, fd)

    # Проверка, что все выполнено корректно
    with open(os.path.join('.', 'data', json_filename), 'r') as fd:
        new_map_json = json.load(fd)
    assert list(new_map_json.keys()) == ['all_map_names', 'maps_numb', 'ru_map_names']

    return 0


def create_path_structure():
    '''
    '''
    if not os.path.exists(os.path.join('.', 'data')):
        os.mkdir(os.path.join('.', 'data'))
        assert os.path.exists(os.path.join('.', 'data')), 'Cannot create dir'
        return -1

    if not os.path.exists(os.path.join('.', 'data', 'templates')):
        os.mkdir(os.path.join('.', 'data', 'templates'))

    if not os.path.exists(os.path.join('.', 'data', 'video_initial')):
        os.mkdir(os.path.join('.', 'data', 'video_initial'))

    if not os.path.exists(os.path.join('.', 'data', 'video_to_add')):
        os.mkdir(os.path.join('.', 'data', 'video_to_add'))

    return 0
