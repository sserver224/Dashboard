from tkinter import *
from tkinter.ttk import *
from tk_tools import *
from psutil import *
from time import sleep as wait
from tkinter import messagebox
from datetime import datetime
root=Tk()
s = Style(root)
battery=DoubleVar()
# add the label to the progressbar style
root.title('Dashboard v1.1 ©sserver')
root.iconbitmap('dashboard.ico')
root.grid()
ram=RotaryScale(root, max_value=100.0,unit='% RAM')
disk=RotaryScale(root, max_value=100.0,unit='% Disk')
clock_hours=SevenSegmentDigits(root, digits=2, background='black', digit_color='blue', height=100)
clock_minutes=SevenSegmentDigits(root, digits=2, background='black', digit_color='blue', height=100)
clock_colon=Label(root, text=':', font=("Segoe UI", 50), background='black', foreground='white')
ram.grid(column=1, row=1)
disk.grid(column=2, row=1)
p = Progressbar(root, orient="vertical", variable=battery)
p_label=Label(background='black', foreground='white', text='')
p_label.grid(column=3, row=2)
p.grid(column=3, row=1)
clock_hours.grid(column=4, row=1)
lo_bat=Led(root, size=20)
lo_bat.grid(column=4, row=2)
Label(root, text='Lo Batt when lit').grid(column=4, row=3)
top=Checkbutton(root, text='Keep on top')
top.grid(column=1, row=2)
top.state(['!alternate'])
clock_minutes.grid(column=6, row=1)
clock_colon.grid(column=5, row=1)
root.config(bg='black')
root.resizable(False, False)
while True:
    try:
        ram.set_value(int(virtual_memory().percent))
        battery.set(int(sensors_battery().percent))
        lo_bat.to_red(on=(int(sensors_battery().percent)<17))
        disk.set_value(int(disk_usage('/').percent))
        d=datetime.now()
        clock_hours.set_value(str(int(d.strftime('%I'))))
        p_label.config(text='Battery '+str(int(battery.get()))+'%')
        clock_minutes.set_value(d.strftime('%M'))
        root.attributes('-topmost', top.instate(['selected']))
        root.update()
        wait(0.01)
    except:
        break
