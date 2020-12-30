import win32com.client as w32
import os
from os import listdir
import re
from tkinter import *
from PIL import ImageTk, Image

def unique(dir):
    u = []
    for s in listdir(dir):
        c = re.search('_final\.', s)
        if c != None:
            continue
        f = re.search('\D\.psd', s)
        if f != None:
            u.append(s[:-4])
    return u

def group(dir):
    dups_list = []
    for u in unique(dir):
        dups = []
        for s in listdir(dir):
            if s[-10:-4] != '_final':
                f = re.search('{}'.format(u), s)
                if f != None:
                    dups.append(s)
        dups_list.append(dups)
    return dups_list

def final(dir):
    to_png = []
    for dups in group(dir):
        if len(dups) > 1:
            for file in dups[:-1]:
                if file not in e2.get().split(', '):
                    os.remove(dir + '/{}'.format(file))
            to_png.append(dups[-1])
        os.rename(dir + '/{}'.format(dups[-1]), dir + 
                  '/{}_final.psd'.format(dups[-1][:-4]))              
    for f in range(len(to_png)):
        to_png[f] = dir + '/' + to_png[f][:-4] + '_final.psd'
    return to_png

def view():
    view_lab = Label(root, text='')
    view_lab.grid(row=5, column=2)
    f_list = []
    for dups in group(e.get()):
        if len(dups) > 1:
            for file in dups[:-1]:
                f_list.append(file)
    view_lab = Label(root, text='Will be deleted:\n' + '\n'.join(f_list))
    view_lab.grid(row=5, column=2)

def clean():
    ps = w32.Dispatch("Photoshop.Application")
    ps.Visible = False
    options = w32.Dispatch('Photoshop.ExportOptionsSaveForWeb')
    options.Format = 13   
    options.PNG8 = False
    for file in final(e.get()):
        psd_file = ps.Open(file)   
        png = '{}.png'.format(file[:-4])
        psd_file.Export(ExportIn=png, ExportAs=2, Options=options)
        psd_file.Close(2)
    ps.Quit()
    l = Label(root, text='Done!')
    l.grid(row=5, column=3)

def view_png():
    global img
    img = Image.open(e.get() + '/' + e3.get() + '.png')
    img = img.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    l_img = Label(root, image=img)
    l_img.grid(row=9, column=1, columnspan=3)
    
def view_final():
    fins = []
    for s in listdir(e.get()):
        c = re.search('_final\.', s)
        if c != None:
            fins.append(s)
    view_lab = Label(root, text='Final versions:\n' + '\n'.join(fins))
    view_lab.grid(row=5, column=1)
    
root = Tk()
root.title('CleanUp')

l1 = Label(root, text=' ', width=50)
l1.grid(row=0, column=1, columnspan=2)
l3 = Label(root, text=' ', width=50)
l3.grid(row=3, column=1, columnspan=2)
lab = Label(root, width=40, text='Enter path to the folder:')
lab.grid(row=2, column=1)
l5 = Label(root, width=40, text='If you don\'t want to remove a file, specify it\'s name:')
l5.grid(row=6, column=1)
l6 = Label(root, width=40, text='To view a file, enter it\'s name here:')
l6.grid(row=7, column=1)

e = Entry(root, width=80)
e.grid(row=2, column=2, columnspan=2)
e2 = Entry(root, width=80)
e2.grid(row=6, column=2, columnspan=2)
e3 = Entry(root, width=80)
e3.grid(row=7, column=2, columnspan=2)

f_but = Button(root, width=40, text='View final files', command=view_final)
f_but.grid(row=4, column=1)
v_but = Button(root, width=40, text='View files to be deleted', command=view)
c_but = Button(root, width=40, text='Clean', command=clean, bg='#96E7A3')
v_but.grid(row=4, column=2)
c_but.grid(row=4, column=3)
img_but = Button(root, text='View', command=view_png)
img_but.grid(row=8, column = 1, columnspan=3)

root.mainloop()
