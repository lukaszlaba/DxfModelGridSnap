import ezdxf
import os

from consolemenu import *
from consolemenu.items import *

try:
    raw_input
except:
    raw_input = input

_version = '0.0.2'
_date = '2018-04-12'
_appname = 'DxfModelGridSnap %s'%_version
_app_dir = os.path.dirname(os.path.abspath(__file__))

menu = ConsoleMenu('%s - manu glowne'%_appname)

grid = 50.0
dir_path = _app_dir
dxf_filename = 'model.dxf'

def dim_round(dim = 50.0, tolerance = 10.0):
    dim = float(dim)
    return round(round(dim/tolerance+0.01) * tolerance)
    
def cord_round(cord=(1.3, 4.8, 6.1), grid=50):
    new_cord = [None, None, None]
    new_cord[0] = dim_round(cord[0], grid)
    new_cord[1] = dim_round(cord[1], grid)
    new_cord[2] = dim_round(cord[2], grid)
    return tuple(new_cord)

def set_dir():
    global dir_path
    path = raw_input('\nPodaj sicezke katalogu:\n')
    if os.path.isdir(path):
        print ('Ok katalog istnieje')
        dir_path = path
    else:
        print ('Nie ma takiego katalogu, sprubuj ponownie')
    pause()    
    
def set_file():
    global dxf_filename
    print ('Jestes w katalogu %s'%dir_path)
    path = raw_input('\nPodaj nazwe pliku dxf:\n')
    if os.path.isfile(os.path.join(dir_path, path)):
        print ('Ok plik istnieje')
        dxf_filename = path
    else:
        print ('Nie ma takiego pliku, sprubuj ponownie')
    pause()
    
def set_grid():
    global grid
    value = raw_input('\nPodaj grid:\n')
    try:
        grid = float(value)
        print ('Ok, grid zmieniony')
    except:
        print ('Chyba nie podales liczby, sprubuj ponownie')
    pause()
    

def show_data():
    print ('Katalog - %s'%dir_path)
    print ('Plik - %s'%dxf_filename)
    print ('grid - %s'%grid)
    pause()

def dxf_filepath():
    return os.path.join(dir_path, dxf_filename)

def transform():
    if os.path.isfile(dxf_filepath()):
        DWG = ezdxf.readfile(dxf_filepath())

        DXF_LINES = []
        
        for e in DWG.modelspace():
            if e.dxftype() == 'LINE':
                #print e
                DXF_LINES.append(e)
        
        for line in DXF_LINES:
            line.dxf.start = cord_round(line.dxf.start, grid)
            line.dxf.end = cord_round(line.dxf.end, grid)
            if line.dxf.start == line.dxf.end:
                DWG.modelspace().delete_entity(line)
                #! Linia zerowa usunieta
            
        ile = len(DXF_LINES)
        #! Znaleziono var_ile line i zaokraglono do grid val_grid
            
        filename = os.path.basename(dxf_filepath())
        new_filname = filename.replace('.dxf', '_ongrid%s.dxf'%int(grid))
        new_path = dxf_filepath().replace(filename, new_filname)
        zapis = True #<<< - wykonanie zapisu
        if zapis :
            try:
                pass
                DWG.saveas(new_path)
                print ('Zapisano zmiany w %s'%new_path)
            except:
                pass
                print ('Problem z zapisam - zamknij plik')
    else:
        print ('!!!!Nie ma pliku %s!!!'%dxf_filepath())
    pause()


def pause():
    raw_input('\n                         (Nacisni Enter aby kontynuowac)\n')
    
#---

def info():
    info = '''
----------------------------------------------
DxfModelGridSnap
ver. %s date: %s
Copyright (C) 2018, Lukasz Laba
----------------------------------------------
'''%(_version, _date)
    print info
    pause()


if __name__ == '__main__':
    menu.append_item(FunctionItem('Wybierz katalog', set_dir, []))
    menu.append_item(FunctionItem('Wybierz plik dxf', set_file, []))
    menu.append_item(FunctionItem('Definiuj grid', set_grid, []))
    menu.append_item(FunctionItem('Pokaz aktualne dane', show_data, []))
    menu.append_item(FunctionItem('Wykonaj zaokraglenie wspolrzednych w wybranym pliku', transform, []))
    menu.append_item(FunctionItem('O programie', info, []))
    #---
    menu.show()