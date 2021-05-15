from psutil import virtual_memory, sensors_battery, disk_usage
from tkinter.ttk import Label, Progressbar, Checkbutton
from tk_tools import RotaryScale, SevenSegmentDigits
from tkinter import Tk, DoubleVar, messagebox
from datetime import datetime
from time import sleep
import sys


root = Tk()

if len(sys.argv) == 2:
    if sys.argv[1] == '-ram_display':
        ram_display = True
        ram = RotaryScale(root, max_value=virtual_memory().total / 1000000000, unit='GB RAM')
    else:
        ram_display = False
        ram = RotaryScale(root, max_value=100.0, unit='% RAM')
else:
    ram = RotaryScale(root, max_value=100.0, unit='% RAM')
    ram_display = False

battery = DoubleVar()

# Add the label to the progressbar style
root.title('Dashboard v1.2 ©sserver')
root.iconbitmap('dashboard.ico')
root.grid()

disk = RotaryScale(root, max_value=100.0, unit='% Disk')
clock_hours = SevenSegmentDigits(root, digits=2, background='black', digit_color='blue', height=100)
clock_minutes = SevenSegmentDigits(root, digits=2, background='black', digit_color='blue', height=100)
clock_colon = Label(root, text=':', font=("Segoe UI", 50), background='black', foreground='white')

ram.grid(column=1, row=1)
disk.grid(column=2, row=1)

p = Progressbar(root, orient="vertical", variable=battery)
p_label = Label(background='black', foreground='white', text='')
p_label.grid(column=3, row=2)
p.grid(column=3, row=1)
clock_hours.grid(column=4, row=1)

top = Checkbutton(root, text='Keep on top')
top.grid(column=1, row=2)
top.state(['!alternate'])
clock_minutes.grid(column=6, row=1)
clock_colon.grid(column=5, row=1)

root.config(bg='black')
root.resizable(False, False)

while True:
    try:
        if ram_display:
            ram.set_value(int(virtual_memory().used / 1000000000))
        else:
            ram.set_value(int(virtual_memory().percent))
        if hasattr(sensors_battery(), 'percent'):
            battery.set(int(sensors_battery().percent))
            if sensors_battery().power_plugged:
                if battery.get() == 100:
                    p_label.config(text=' Fully charged  ')
                else:
                    p_label.config(
                        text='Charging ' + ('  ' * (3 - len(str(int(battery.get())))) + str(int(battery.get())) + '%'))
            else:
                p_label.config(
                    text='  Battery ' + ('  ' * (3 - len(str(int(battery.get())))) + str(int(battery.get())) + '%  '))
        else:
            p_label.config(text='No batt present')
            battery.set('0')
        disk.set_value(int(disk_usage('/').percent))
        d = datetime.now()
        clock_hours.set_value(str(int(d.strftime('%I'))))
        clock_minutes.set_value(d.strftime('%M'))

        root.attributes('-topmost', top.instate(['selected']))
        root.update()
        sleep(0.01)
    except Exception:
        break
