#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import os
import json
import numpy as np
import pandas as pd

from typing import Optional


# In[ ]:





# In[ ]:





# In[2]:


class CreateTemplatesClass():
    def __init__(self, inp_data_path: Optional[str]='', 
                       inp_video_path: Optional[str]='', 
                       inp_templates_path: Optional[str]='', 
                ) -> None:
        if inp_data_path != '':
            self.__DATA_PATH = inp_data_path
        else:
            self.__DATA_PATH = os.path.join('.', 'data')

        if inp_video_path != '':
            self.__VIDEO_PATH = inp_video_path
        else:
            self.__VIDEO_PATH = os.path.join(self.__DATA_PATH, 'video_initial')

        if inp_templates_path != '':
            self.__TEMPLATES_PATH = inp_templates_path
        else:
            self.__TEMPLATES_PATH = os.path.join(self.__DATA_PATH, 'templates')

        self.__tqdm_disable = False



    def preload_info(self, ) -> None:
        with open(os.path.join(self.__DATA_PATH, 'maps_info.json'), 'r') as fd:
            map_info = json.load(fd)
            self.__ALL_MAP_NAMES = map_info['all_map_names']

        path_to_map_info = os.path.join(self.__DATA_PATH, 'prepared_maps_info.csv')
        if not os.path.exists(path_to_map_info):
            print('Retire!')
        else:
            self.__map_info_df = pd.read_csv(path_to_map_info)
            #self.__map_info_df.shape



    def set_tqdm(self, inp_val: bool) -> None:
        self.__tqdm_disable = inp_val



    def get_param(self, param_name: str):
        if f'_CreateTemplatesClass{param_name}' in self.__dict__.keys():
            return self.__dict__[f'_CreateTemplatesClass{param_name}']
        else:
           return 'У класса нат запрашиваемого параметра.'



    def cut_frame(self, inp_frame: np.ndarray, inp_type: str) -> np.ndarray:
        # now only for resolution 1920 x 1080
        # and max mini map size
        if inp_type == 'map_name':
            inp_frame = inp_frame[260:339, 816:902, :]   # recheck for all map names [260:339, 816:912, :]
        elif inp_type == 'battle_type':
            inp_frame = inp_frame[259:339, 1018:1416, :] # recheck for all battle types 259:339, 1010:1416, :]
        elif inp_type == 'battle_type_icon':
            inp_frame = inp_frame[251:348, 912:1010, :]
        elif inp_type =='map_upper_plank':
            inp_frame = inp_frame[-626:-612, -626:, :]
        elif inp_type == 'start_frame':
            tmp_frame_allies  = inp_frame[340:378, 462:738, :]
            tmp_frame_enemies = inp_frame[340:378, 1186:1462, :]
            inp_frame = np.concatenate((tmp_frame_allies, tmp_frame_enemies))
        elif inp_type == 'battle_data_start_allies':
            inp_frame = inp_frame[340:730, 460:740, :]
        elif inp_type == 'battle_data_start_enemies':
            inp_frame = inp_frame[340:730, 1186:1462, :]
        elif inp_type == 'results':
            inp_frame = inp_frame#[340:730, 1186:1462, :]
        else:
            return inp_frame
    
        return inp_frame



    def generate_frames(self, 
                        inp_map: str, 
                        start: int, 
                        inp_type: str,
                        max_idx: Optional[int] = 2000,
                        inp_sub_path: Optional[str] = '', 
                        max_file_idx: Optional[int] = 20, 
                       ) -> int:
    
    
        if inp_sub_path != '':
            path_to_save = os.path.join(TEST_FRAMES, inp_sub_path)
        else:
            path_to_save = os.path.join(TEST_FRAMES, inp_map)
        print(path_to_save)
    
        if not os.path.exists(path_to_save):
            #print(f'Path {path_to_save} not exists. Please create it before new start.')
            print(f'Путь {path_to_save} не существует. Создаю.')
            os.mkdir(path_to_save)
            if not os.path.exists(path_to_save):
                return -1
    
        idx = 0
        for el in self.__map_info_df.iterrows():
            filename = f'{el[1]["map_name"]}_{el[1]["battle_type"]}.mp4'
            if inp_map.lower() != 'all':
                if not inp_map.lower() in filename:
                    print(f'Пропускаю {filename}')
                    continue
    
            if start == 0: 
                start_time = 0
                end_time = el[1]['battle_start']
            elif start == 1:
                start_time = el[1]['battle_start']
                end_time = el[1]['battle_end']
            else:
                start_time = el[1]['battle_end']
                end_time = el[1]['duration']
    
            video = cv2.VideoCapture(os.path.join(self.__VIDEO_PATH, filename))
            fps = video.get(cv2.CAP_PROP_FPS)
            max_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    
            file_idx = 0
            for index in tqdm(range(start_time + 1, (end_time - 1)*3),  
                              desc=filename, disable = self.__tqdm_disable,
                              leave=False):
                offset = int(index * fps / 3)
                if offset > max_frames:
                    print(f'Too big offset {offset} vs {max_frames}')
                    continue
    
                video.set(cv2.CAP_PROP_POS_FRAMES, offset)
                _, frame = video.read()
                frame = cut_frame(frame, inp_type)
                if inp_sub_path != '':
                    cv2.imwrite(os.path.join(path_to_save, f'{inp_sub_path}_{idx}.png'), frame)
                else:
                    cv2.imwrite(os.path.join(path_to_save, f'{inp_map}_{idx}.png'), frame)
    
                idx += 1
                file_idx += 1
                if (max_idx > 0 and idx >= max_idx) or \
                    file_idx > max_file_idx:
                    print('exit on max idx')
                    return 0
            
        return 0



        def create_aver(self, inp_path: str):

            if not os.oath.exists(inp_path):
                print('Заланный путь не сушествует / Не ыерно задан путь.')
                return -1

            all_files = os.listdir(inp_path)
            if len(all_files) == 0:
                print('Пустая папка. Нет кадров для усреднения.')
                return -1

            
            return 0


# In[ ]:





# In[3]:


crete_templates = CreateTemplatesClass()


# Загружаю имена всех карт

# In[4]:


crete_templates.preload_info()


# In[7]:


#crete_templates.get_param('__ALL_MAP_NAMES')


# In[8]:


#crete_templates.get_param('__map_info_df')


# In[ ]:





# generate_frames(inp_df: pd.DataFrame,  
#                     inp_map: str,  
#                     start: int,  
#                     inp_type: str,  
#                     max_idx: Optional[int] = 2000,  
#                     inp_sub_path: Optional[str] = '',   
#                     max_file_idx: Optional[int] = 20,  
#                    ) -> int:

# In[11]:


BATTLE_TYPES = ['assault', 'counter', 'standart']


# In[ ]:


for el in BATTLE_TYPES:
    crete_templates.generate_frames(, )

