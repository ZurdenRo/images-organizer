from codecs import Codec, StreamReader, StreamWriter
from multiprocessing import Pool
import os
from datetime import datetime
from enum import Enum
from shutil import copy2, copy
import logging

"""
    1. Setear carpeta de busqueda
    2. Seleccion solo archivos tipo imagenes(.jpg, .jpeg, .heic)
    3. Guardar en un array, obtener fecha de creacion de archivo, 
        Ordenar los archivos por year and month
    6. Verificar ano, verificar si existe tal carpeta con ano, si no, crear carpeta ano.
    7. ingresar dentro de la carpeta, verificar si existe mes, si no, crear carpeta mes.
    8. guardar archivo dentro de la carpeta ano con su correspondiente mes. 

"""
# this folder can delete it
PATH = r"D:\Usuarios\Rodrigo\Documents\BackUp CelularesViejos\Memoria NEXUS6P\FOTOS DE MI CAMARA"
_PATH_TEST = r"D:\Usuarios\Rodrigo\Documents\BackUp CelularesViejos\Memoria NEXUS6P\TEST"


class Month(Enum):
    JENUARY = 1
    FEBREARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

def select_only_images(my_dict):
    for file in os.scandir(PATH):
       if file.is_file:     
        tuple_file = os.path.splitext(file.name) 
        if tuple_file[1] == '.jpg':
                m_time = os.path.getmtime(file) 
                time_modified = datetime.fromtimestamp(m_time)
                var_year = str(time_modified.year)
                var_month = get_month(time_modified.month)
                key = '-'.join([var_year, var_month])
                value = my_dict.get(key)
                if value == None:
                    my_dict[key] = [file]
                else:
                    value.append(file)
        elif tuple_file[1] == '.HEIC':
                pass  
    


def get_month(number_month: int) -> str:
    match number_month:
        case Month.JENUARY.value:
            return Month.JENUARY.name
        
        case Month.FEBREARY.value:
            return Month.FEBREARY.name
        
        case Month.MARCH.value:
            return Month.MARCH.name
        
        case Month.APRIL.value:
            return Month.APRIL.name
        
        case Month.MAY.value:
            return Month.MAY.name
        
        case Month.JUNE.value:
            return Month.JUNE.name
        
        case Month.JULY.value:
            return Month.JULY.name
        
        case Month.AUGUST.value:
            return Month.AUGUST.name
        
        case Month.SEPTEMBER.value:
            return Month.SEPTEMBER.name
        
        case Month.OCTOBER.value:
            return Month.OCTOBER.name
        
        case Month.NOVEMBER.value:
            return Month.NOVEMBER.name
        
        case Month.DECEMBER.value:
            return Month.DECEMBER.name
        
        case _:
            return 'ERROR'

def create_folders():
    # exist folder year? no -> create folder year -> create folder month -> put file in folder
    # exist folder year? yes -> exist folder month? no -> create folder month -> put file in folder
    # exist folder year? yes -> exist folder month? yes -> put file in folder

    # 1. create folders years and months
    for key in my_dict:
        print(key)
        create_folder_year = True
        create_folder_month = True
        for file in os.scandir(_PATH_TEST):
            if file.is_dir:
                print(file.name)

                if file.name == key.split('-')[0]:
                    create_folder_year = False
                    print(file.path)
                    for f in os.scandir(file.path):
                        if f.is_dir:
                            print(f.name)
                            print(key.split('-')[1])
                            if f.name == key.split('-')[1]:
                                create_folder_month = False
                                # if true create folder month
                            if create_folder_month:
                                os.mkdir(_PATH_TEST + r'\\' + key.split('-')[0] + r'\\' + key.split('-')[1]) 
                                path_str = _PATH_TEST + r'\\' + key.split('-')[0] + r'\\' + key.split('-')[1]
                                # copy files to dst folder
                                put_files_in_folder(key, path_str)
                                break                                                 
        
        if create_folder_year:
            # create year folder
            os.mkdir(_PATH_TEST + r'\\' + key.split('-')[0])
            # create month folder
            os.mkdir(_PATH_TEST + r'\\' + key.split('-')[0] + r'\\' + key.split('-')[1])
            path_str = _PATH_TEST + r'\\' + key.split('-')[0] + r'\\' + key.split('-')[1]
            # copy files to dst folder
            put_files_in_folder(key, path_str)


def put_files_in_folder(key, dst_path):
    # 2. move files in respective folders
    array = my_dict.get(key)
    for f in array:
        copy2(f, dst_path)


def move_images(dct: dict):
    key_ls = list(dct)
    final = len(key_ls)
    init = 0
    while init < final:
        list_images = dct.get(key_ls[init])
        list_dir_years = list(os.scandir(_PATH_TEST))
        year_name = key_ls[init].split('-')[0]
        month_name = key_ls[init].split('-')[1]
        exist_folder_year = find_folder_year(list_dir_years, year_name, len(list_dir_years))

        if exist_folder_year:
            abs_path = os.path.join(_PATH_TEST, year_name)
            list_dir_months = list(os.scandir(abs_path))
            exist_folder_month = find_folder_month(list_dir_months, month_name, len(list_dir_months))
        else:
            exist_folder_month = False

        dst_images = os.path.join(_PATH_TEST, year_name, month_name)

        if exist_folder_year and exist_folder_month:
            move_images_in_folder(list_images, dst_images) # put images inside exactly folders
        elif exist_folder_year and not exist_folder_month:
            os.mkdir(dst_images)
            move_images_in_folder(list_images, dst_images)
        else:
            os.mkdir(os.path.join(_PATH_TEST, year_name))
            os.mkdir(dst_images)
            move_images_in_folder(list_images, dst_images)
        init = init + 1

def recursive_searching(path, my_dict):
    iter = os.scandir(path)
    for _fsystem in iter:
        if _fsystem.is_dir(): 
            print(_fsystem.path)
            recursive_searching(_fsystem.path, my_dict)
        else:
            _stat_modified = os.stat(_fsystem.path).st_mtime
            _time_modified = datetime.fromtimestamp(_stat_modified)
            year = str(_time_modified.year)
            month = get_month(_time_modified.month)
            key = '-'.join([year, month])
            if os.path.splitext(_fsystem.path)[1] == '.jpg':        
                value = my_dict.get(key)
                if value == None:
                    my_dict[key] = [_fsystem]
                else:
                    value.append(_fsystem)
            elif os.path.splitext(_fsystem.path)[1] == '.HEIC':
                value = my_dict.get(key)
                if value == None:
                    my_dict[key] = [_fsystem]
                else:
                    value.append(_fsystem)

def find_folder_year(path, key, final):
    x = 0
    while x < final:
        if path[x].name == key:
            return True
        x = x + 1
    return False
        
def find_folder_month(path, key, final):
    x = 0
    while x < final:
        if path[x].name == key:
            return True
        x = x + 1
    return False

def move_images_in_folder(array_images, dst_path):
    for img in array_images:
        copy2(img, dst_path)

def organize_by_threads(key):
        list_images = my_dict[key]
        list_dir_years = list(os.scandir(_PATH_TEST))
        year_name = key.split('-')[0]
        month_name = key.split('-')[1]
        exist_folder_year = find_folder_year(list_dir_years, year_name, len(list_dir_years))

        if exist_folder_year:
            abs_path = os.path.join(_PATH_TEST, year_name)
            list_dir_months = list(os.scandir(abs_path))
            exist_folder_month = find_folder_month(list_dir_months, month_name, len(list_dir_months))
        else:
            exist_folder_month = False
        
        dst_images = os.path.join(_PATH_TEST, year_name, month_name)

        if exist_folder_year and exist_folder_month:
            move_images_in_folder(list_images, dst_images) # put images inside exactly folders
        elif exist_folder_year and not exist_folder_month:
            os.mkdir(dst_images)
            move_images_in_folder(list_images, dst_images)
        else:
            os.mkdir(os.path.join(_PATH_TEST, year_name))
            os.mkdir(dst_images)
            move_images_in_folder(list_images, dst_images)

if __name__ == "__main__":  
    my_dict = dict()
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
    start = datetime.now()
    recursive_searching(PATH, my_dict)
    move_images(my_dict)
    end = datetime.now()
    final = end - start
    logging.info("result: %s", final.total_seconds())
    







    
