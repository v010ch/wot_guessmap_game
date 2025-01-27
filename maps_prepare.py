#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import json
#import numpy as np
import os
import time
from typing import Optional
#from tqdm.notebook import tqdm

import cv2
import pandas as pd


# In[ ]:





# In[2]:


DATA_PATH = os.path.join('.', 'data')


# In[ ]:





# In[ ]:





# In[3]:


COLS = ['map_name', 'battle_type', 'sub_number',
        'hard_level', 'tank_levels', 'base',
        'duration', 'frame_count',
        'battle_start', 'countdown',
        'battle_end', 'results',
        'parent_map',
]


# In[4]:


class MapPrepareClass():
    def __init__(self, wrk_folder: Optional[str] = ''):
        if wrk_folder != '':
            ## SECURE PATH WITH from werkzeug.utils import secure_filename??
            self.__DATA_PATH = os.path.join('.', wrk_folder)
        else:
            self.__DATA_PATH = os.path.join('.', 'data')
        self.__VIDEO_PATH = os.path.join(self.__DATA_PATH, 'video_initial')
        self.__NEW_VIDEO_PATH = os.path.join(self.__DATA_PATH, 'video_to_add')

        if not os.path.exists(self.__DATA_PATH):
            os.mkdir(self.__DATA_PATH)
            print(f'created path: {self.__DATA_PATH}')
        if not os.path.exists(self.__VIDEO_PATH):
            os.mkdir(self.__VIDEO_PATH)
            print(f'created path: {self.__VIDEO_PATH}')
        if not os.path.exists(self.__NEW_VIDEO_PATH):
            os.mkdir(self.__NEW_VIDEO_PATH)
            print(f'created path: {self.__NEW_VIDEO_PATH}')

        self.__add_all = False
        pass



    def set_add_all(self, inp_val: bool):
        self.__add_all = inp_val
        return 0



    def __calc_max_subnumbers(self, is_new: bool = True):

        if is_new:
            self.__max_subidx = {}
            #for el in product(MAP_NAMES, BATTLE_TYPES):
            #    self.__max_subidx["_".join(el)] = 0
        else:
            if os.path.exists(os.path.join(DATA_PATH, 'max_subidx.json')):
                with open(os.path.join(DATA_PATH, 'max_subidx.json'), 'r+') as fd:
                    self.__max_subidx = json.load(fd)
            else:
                print('error: map_status.json is absent!')

        return 0



    def __add_new_map_bt_dialogue(self, map_name: str, map_type: str) -> bool:

        if self.__add_all:
            return True

        print('Обнаружена новая пара имя_карты - тип_битвы:')
        print("_".join((map_name, map_type)))
        print('Добавить?')
        val = input('[y] - добавить / [n] - пропустить')

        if len(val) > 3:
            val = val[:3]

        if val == 'y' or val == 'yes' or val == 'add':
            return True
        elif val == 'n' or val == 'no':
            return False
        else:
            print('Выбран неизвестный вариант. Пропускаю.')
            print('Вы можете добавить эту пару позднее.')
            return False
        
        

    def add_initial_maps(self, del_original: Optional[bool]=True) -> int:

        maps_to_add = os.listdir(self.__NEW_VIDEO_PATH)
        if len(maps_to_add) == 0:
            print('Nothing to add')
            return 0

        if os.path.exists(os.path.join(DATA_PATH, 'prepared_maps_info.csv')):
            prepared_maps_info = pd.read_csv(os.path.join(DATA_PATH, 'prepared_maps_info.csv'))
            self.__calc_max_subnumbers(False)
        else:
            prepared_maps_info = pd.DataFrame(columns=COLS)
            self.__calc_max_subnumbers(True)

        tmp_df = pd.DataFrame(columns=COLS, index=range(len(maps_to_add)))
        idx = 0
        for el in maps_to_add:
            info = self.get_video_info(el)
            map_name = info['map_name']
            battle_type = info['battle_type']
            print(map_name, battle_type)
            #subnumber = self.__max_subidx["_".join((map_name, map_type))]
            if "_".join((map_name, battle_type)) not in self.__max_subidx.keys():
                add = self.__add_new_map_bt_dialogue(map_name, battle_type)
                if not add:
                    continue
                else:
                    self.__max_subidx["_".join((map_name, battle_type))] = 0
                
            subnumber = self.__max_subidx["_".join((map_name, battle_type))]
            #tmp_df.loc[idx] = {'map_name': map_name,
            #                   'battle_type': map_type, 
            #                   'sub_number':  subnumber,
            #                  }
            info['sub_number'] = subnumber
            tmp_df.loc[idx] = info
            self.__max_subidx['_'.join((map_name, battle_type))] += 1
            new_filename = f'{map_name}_{battle_type}_{str(subnumber).zfill(5)}.mp4'
            os.rename(os.path.join(self.__NEW_VIDEO_PATH, el), 
                      os.path.join(self.__NEW_VIDEO_PATH, new_filename)
                     )
            idx += 1

        tmp_df.dropna(axis=0, how='all', inplace=True)
        prepared_maps_info = pd.concat((prepared_maps_info, tmp_df))
        #print(tmp)
        #print(self.__max_subidx)
        with open(os.path.join(DATA_PATH, 'max_subidx.json'), 'w') as fd:
            json.dump(self.__max_subidx, fd)
        prepared_maps_info.to_csv(os.path.join(DATA_PATH, 'prepared_maps_info.csv'), index=False)

        # copy to dest folder with next index

        return 0



    def get_video_info(self, inp_filename: str) -> dict:
        # rewwrite to getting from video frames
        ret = {el: '' for el in COLS}
        
        tmp = inp_filename.split('.')[0]. \
                           split('_')[:-1]
        ret['map_name'] = '_'.join(tmp).lower()
        ret['battle_type'] = inp_filename.split('.')[0]. \
                                          split('_')[-1].\
                                          split('(')[0].\
                                          strip().\
                                          lower()

        tmp = cv2.VideoCapture(os.path.join(self.__NEW_VIDEO_PATH, inp_filename))
        ret['frame_count'] = int(tmp.get(cv2.CAP_PROP_FRAME_COUNT))
        tmp.release()
        time.sleep(0.1)
        
        return ret


# In[ ]:





# In[5]:


#COLS


# In[6]:


map_prepare = MapPrepareClass()


# In[7]:


map_prepare.set_add_all(True)


# In[8]:


map_prepare.add_initial_maps()


# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:


41-16


# In[ ]:




