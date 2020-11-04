#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pylab
import skrf as rf
from skrf import NetworkSet

from tkinter import *
from tkinter.filedialog import askopenfilenames

OPTIONS = []
PLOT_NUMBER = []
select_box = []
plot = []

values_to_plot = []

root = Tk()
root.title("VNA plotter V.1.0")

# setting the minimum size of the root window
root.minsize(300, 150) 
root.iconbitmap('src\images\icon.ico')

root.withdraw() # remove the window
filename = askopenfilenames(title='Choose a file') # show an "Open" dialog box and return the path to the selected file
root.deiconify() # enable the window

def add_plot():
    print('add plot')
    values_to_plot.append(len(select_box))

    addplotframe = Frame(root)
    addplotframe.pack(side = TOP)
    
    label = Label(addplotframe, text=len(select_box))
    label.pack(side = LEFT, expand = YES)
    
    variable = StringVar(addplotframe)
    variable.set(OPTIONS[0])
    option_menu = OptionMenu(addplotframe, variable, *OPTIONS)
    option_menu.pack(side = LEFT, expand = YES)

    variable2 = StringVar(addplotframe)
    variable2.set(PLOT_NUMBER[0])
    plot_menu = OptionMenu(addplotframe, variable2, *PLOT_NUMBER)
    plot_menu.pack(side = LEFT, expand = YES)

    select_box.append(variable)
    plot.append(variable2)


def remove_plot():
    list = root.pack_slaves()
    #print(list)
    if (len(list) > 3):
        list[-1].destroy()
        values_to_plot.pop()


def plot_values():
    for i in range(len(select_box)):        
        print ("value is: " + select_box[i].get())

    print(select_box)

    root.withdraw() # remove the window

    for file in range(len(sp_value)):
        for i in range(len(values_to_plot)):
            val = select_box[i].get()
            m = int(val[1]) - 1
            n = int(val[2]) - 1
            print(n,m)

            # plot magnitude (in db)
            print('Creating plot {}, trace {}, port used {}'.format(i, file, val))
            pylab.figure(plot[i].get())                    
            #pylab.title('Return Loss (Mag)')
            sp_value[file].plot_s_db(m=m,n=n) # m,n are S-Matrix indices

    pylab.show()
    print("End")
    root.destroy()
    

def plot_all():
    root.withdraw() # remove the window
    
    for i in range(len(sp_value)):
        port_num = len(sp_value[i].s_db[0])
        # print(port_num)
        p = 1
        for x in range(port_num):
            for j in range(port_num):   
                # plot magnitude (in db)
                print('Creating plot {}, trace {}, port used {}'.format(p, i, port_num))
                pylab.figure(p)
                p += 1
                    
                #pylab.title('Return Loss (Mag)')
                sp_value[i].plot_s_db(m=x,n=j) # m,n are S-Matrix indices

    pylab.show()
    print("End")
    root.destroy()


btnframe = Frame(root)
btnframe.pack(side = TOP)
    
btn_plot_all = Button(btnframe, text="Plot all", command=plot_all)
btn_plot_all.pack(side = LEFT, anchor = N, expand = YES)

btn_remove_plot = Button(btnframe, text="Remove plot", command=remove_plot)
btn_remove_plot.pack(side = LEFT, anchor = N, expand = YES)

btn_add_plot = Button(btnframe, text="Add plot", command=add_plot)
btn_add_plot.pack(side = LEFT, anchor = N, expand = YES)

btn_continue = Button(root, text="CONTINUE", command=plot_values)
btn_continue.pack(side = BOTTOM, anchor = S, expand = YES)

print('Start program')
print('Load file/s')

sp_value = []
for i in range(len(filename)):
    f_name = filename[i]
    print('Open:', f_name)   
    f_name.encode(encoding='UTF-8',errors='strict')
    sp_value.append(rf.Network(f_name))

print('File/s loaded')

port_num = len(sp_value[i].s_db[0])
print(port_num)

counter = 0
for x in range(port_num):
    for j in range(port_num):
        val = 'S' + str(x + 1) + str(j + 1)
        counter += 1
        OPTIONS.append(val)
        PLOT_NUMBER.append(counter)

# create one plot
add_plot()

root.mainloop()
