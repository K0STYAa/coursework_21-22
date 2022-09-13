# -*- coding: UTF-8 -*-
from logging import exception
import os
import sys
import pandas as pd
from IPython.display import display
import collections

from shingles_algorithm import shingle_compaire_2_files

import time


language_dict = {
    'python': [".py"],
    'C': [".c"],
    'pascal': [".PAS", ".pas"],
    'assembler': [".ASM", ".asm"]
}

lim = 20 # Показатель сходства выше которого программа возвращает совпадающие файлы


def files_list_in_dir (sol_dir, language):

    names = os.listdir(sol_dir)
    endings = language_dict[language]
    filenames_list = []

    for name in names:
        fullname = os.path.join(sol_dir, name)
        if os.path.isfile(fullname):
            for ending in endings:
                if name.endswith(ending):
                    filenames_list.append(fullname)
        if os.path.isdir(fullname):
            filenames_list += files_list_in_dir(fullname, language)

    return filenames_list

def language_identification (sol_dir):
    if os.path.exists(sol_dir):
        names = os.listdir(sol_dir)
        for name in names:
            fullname = os.path.join(sol_dir, name)
            if os.path.isfile(fullname):
                _, file_extension = os.path.splitext(fullname)
                for language, extension_list in language_dict.items():
                    for extension in extension_list:
                        if extension == file_extension:
                            return language
        raise Exception("No program files in directory.")
    else:
        raise Exception("No such directory exists.")


def compaire_all_files_in_dir (sol_dir, language, cod):

    for _ in range(150):
        print("#", end="")
    print("\n")
    print(sol_dir, "\n")
    filenames_list = files_list_in_dir(sol_dir, language)
    for i in range(len(filenames_list)):
        print(i,":", filenames_list[i])

    res = []
    for _ in range(len(filenames_list)):
        res.append([0] * len(filenames_list))

    for filename1_number in range(len(filenames_list)):
        for filename2_number in range(filename1_number, len(filenames_list)):
            if filename1_number != filename2_number:
                new_value = shingle_compaire_2_files(filenames_list[filename1_number], filenames_list[filename2_number], cod, f, lim)
                res[filename1_number][filename2_number] = new_value
                new_dict = collections.Counter()
                new_dict[new_value] = 1
                dict_counter.update(new_dict)

    df = pd.DataFrame(res)
    print()
    display(df)
    print()

    for i in range(len(res)):
        for j in range(len(res[i])):
            if res[i][j] >= lim:
                print(i,":", filenames_list[i])
                print(j,":", filenames_list[j])
                print(res[i][j], "\n")
    

def dir_pascal (sol_dir):

    names = os.listdir(sol_dir)
    filenames_list = []

    for name in names:
        fullname = os.path.join(sol_dir, name)
        if os.path.isdir(fullname):
            if fullname.endswith("Phase1"):
                    filenames_list.append(fullname)
            if fullname.endswith("Phase2"):
                    filenames_list.append(fullname)
            if fullname.endswith("Phase3"):
                    filenames_list.append(fullname)
            filenames_list += dir_pascal(fullname)

    return filenames_list

def dir_asm (sol_dir):

    names = os.listdir(sol_dir)
    filenames_list = []

    for name in names:
        fullname = os.path.join(sol_dir, name)
        if os.path.isdir(fullname):
            if fullname.endswith("HW1"):
                    filenames_list.append(fullname)
            if fullname.endswith("HW2"):
                    filenames_list.append(fullname)
            if fullname.endswith("HW3"):
                    filenames_list.append(fullname)
            if fullname.endswith("HW4"):
                    filenames_list.append(fullname)
            if fullname.endswith("HW5"):
                    filenames_list.append(fullname)
            if fullname.endswith("HW6"):
                    filenames_list.append(fullname)
            if fullname.endswith("P4"):
                    filenames_list.append(fullname)
            if fullname.endswith("P5"):
                    filenames_list.append(fullname)
            if fullname.endswith("ДЗ1"):
                    filenames_list.append(fullname)
            if fullname.endswith("ДЗ2"):
                    filenames_list.append(fullname)
            if fullname.endswith("ДЗ3"):
                    filenames_list.append(fullname)
            if fullname.endswith("ДЗ4"):
                    filenames_list.append(fullname)
            if fullname.endswith("ДЗ5"):
                    filenames_list.append(fullname)
            if fullname.endswith("Строки"):
                    filenames_list.append(fullname)
            if fullname.endswith("Структуры"):
                    filenames_list.append(fullname)
            if fullname.endswith("Сортировка"):
                    filenames_list.append(fullname)
            filenames_list += dir_asm(fullname)

    return filenames_list


def main():

    start_time = time.time()
    
    # choose what to do
    todo = ''
    try:
        todo = sys.argv[1]
        os.system('cls' if os.name == 'nt' else 'clear')
    except IndexError:
        print('Exception. No arguments')
        return

    if todo == 'python': # Python
        sol_dir = 'programs/different_qsort_solutions/'
        compaire_all_files_in_dir(sol_dir, 'python', 'utf-8')

    elif todo == 'pascal': # Pascal
        all_files = dir_pascal("programs")
        all_files.append("programs/Archive/2013-2014/2013/Task4/")
        all_files.append("programs/Archive/2013-2014/2013/Task5/")
        all_files.append("programs/Archive/2017-2018/2017/Task 2/")
        for element in all_files:
            compaire_all_files_in_dir(element, 'pascal', 'cp866')

    elif todo == 'asm': # Asm
        all_files = dir_asm("programs")
        for element in all_files:
            compaire_all_files_in_dir(element, 'assembler', 'cp1251')

    else:
        try:
            sol_dir = 'programs/' + todo 
            language = language_identification(sol_dir)
            compaire_all_files_in_dir(sol_dir, language, 'utf-8')
        except Exception as err: 
            print("Incorrect argument. " + str(err))
    
    my_dict = dict(dict_counter)
    my_time = time.time() - start_time
    print("--- %s seconds ---" % my_time, sum(my_dict.values())/my_time, "comparisons/s")
    print()
    if len(my_dict):
        print(my_dict)


# Start program
f = open("suspects.txt", "w")
dict_counter = collections.Counter()
main()
f.close()