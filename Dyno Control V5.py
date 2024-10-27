import tkinter as tk
from tkinter import scrolledtext
import threading
import serial
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import pandas as pd
import threading

ser = serial.Serial()

root = tk.Tk()
root.title("Dyno Controler and recorder V4") #names the box
root.geometry('2000x1000+50+25') #sets the box size and location


window = tk.Frame(root, bg="white")
window.pack(padx=0, pady=0)

#Stop the frame from propagating the widget to be shrink or fit
#window.grid_propagate(False)

throttle_request_var = tk.IntVar()
mixture_request_var = tk.IntVar()
load_request_var = tk.IntVar()

# serial lines
measurements = []

def throttle_changed(event):
    value = throttle_request_var.get()
    message = f"throttle{value}\r\n"
    print(message.strip())
    ser.write(message.encode())

def kill_throttle():
    throttle_request_var.set(0)
    throttle_changed(None)

def throttle50():
    throttle_request_var.set(50)
    throttle_changed(None)

def throttle100():
    throttle_request_var.set(100)
    throttle_changed(None)    

def mixture_changed(event):
    value = mixture_request_var.get()
    message = f"mixture{value}\r\n"
    print(message.strip())
    ser.write(message.encode())

def load_changed(event):
    value = load_request_var.get()
    message = f"load{value}\r\n"
    print(message.strip())
    ser.write(message.encode())

def kill_load():
    load_request_var.set(0)
    load_changed(None)

def data_chart():
    fig = Figure(figsize = (5, 5),dpi = 100)
    y = [i**2 for i in range(101)]
    plot1 = fig.add_subplot(111) 
    plot1.plot(y)

rpm_label = tk.Label(window, text = "RPM: 000" , fg="green", bg="white", font=("Helvetica", 25), width=15)
rpm_label.grid(column=0, row=2, padx=10, pady=10)

temp1_label = tk.Label(window, text = "Head Temp 000" , fg="black", bg="white", font=("Helvetica", 15), width=20)
temp1_label.grid(column=3, row=1, padx=10, pady=10)

temp2_label = tk.Label(window, text = "Manifold Temp 000" , fg="black", bg="white", font=("Helvetica", 15), width=20)
temp2_label.grid(column=3, row=2, padx=10, pady=10)

temp3_label = tk.Label(window, text = "Air Temp 000" , fg="black", bg="white", font=("Helvetica", 15), width=20)
temp3_label.grid(column=3, row=3, padx=10, pady=10)

load_actual_label = tk.Label(window, text = "Load mV: 000" , fg="green", bg="white", font=("Helvetica", 25), width=10)
load_actual_label.grid(column=2, row=2, padx=10, pady=10)

throttle_label = tk.Label(window, text = "Throttle Control", fg="Black", bg="white", font=("Helvetica", 15))
throttle_label.grid(column=0, row=3, padx=10, pady=10)

mixture_label = tk.Label(window, text = "Mixture Control", fg="Black", bg="white", font=("Helvetica", 15))
mixture_label.grid(column=1, row=3, padx=10, pady=10)

load_label = tk.Label(window, text = "Load Control", fg="Black", bg="white", font=("Helvetica", 15))
load_label.grid(column=2, row=3, padx=10, pady=10)

throttle_scale = tk.Scale(window, from_=0, to=100, variable=throttle_request_var, command=throttle_changed, bg="white", length=500, font=("Helvetica", 16))
throttle_scale.grid(column=0, row=4, padx=10, pady=10)

mixture_scale = tk.Scale(window, from_=0, to=100, variable=mixture_request_var, command=mixture_changed, bg="white", length=500, font=("Helvetica", 16))
mixture_scale.grid(column=1, row=4, padx=10, pady=10)

load_scale = tk.Scale(window, from_=0, to=100, variable=load_request_var, command=load_changed, bg="white", length=500, font=("Helvetica", 16))
load_scale.grid(column=2, row=4, padx=10, pady=10)

throttle_entry = tk.Entry(window, textvariable=throttle_request_var, width=10, font=("Helvetica", 16))
throttle_entry.grid(column=0, row=5, padx=10, pady=10)
throttle_entry.bind('<Return>', throttle_changed)

mixture_entry = tk.Entry(window, textvariable=mixture_request_var, width=10, font=("Helvetica", 16))
mixture_entry.grid(column=1, row=5, padx=10, pady=10)
mixture_entry.bind('<Return>', mixture_changed)

load_entry = tk.Entry(window, textvariable=load_request_var, width=10, font=("Helvetica", 16))
load_entry.grid(column=2, row=5, padx=10, pady=10)
load_entry.bind('<Return>', load_changed)

throttle_reset_button = tk.Button(window, text="Kill Throttle", command=kill_throttle,bg= "darkred" , width=10, height=2, font=("Helvetica", 13, "bold"))
throttle_reset_button.grid(column=0, row=6, padx=10, pady=10)

load_reset_button = tk.Button(window, text="Kill Load", command=kill_load,bg= "darkred" , width=10, height=2, font=("Helvetica", 13, "bold"))
load_reset_button.grid(column=2, row=6, padx=10, pady=10)

serial_monitor_label = tk.Label(window, text = "Serial Monitor", fg="Black", bg="white", font=("Helvetica", 15, "bold"))
serial_monitor_label.grid(column=2, row=8, padx=10, pady=10)

serial_monitor = scrolledtext.ScrolledText(window, width=50, height=4, wrap=tk.NONE, state=tk.DISABLED)
serial_monitor.grid(column=1, row=9, columnspan=5, padx=10, pady=10)

# Create a figure for plotting
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

lines = {
    'throttle_percentage': ax1.plot([], [], 'b-', lw=2, label='Throttle %')[0],
    'load_requested': ax1.plot([], [], 'g-', lw=2, label='Load Requested')[0],
    'load_actual': ax1.plot([], [], 'r-', lw=2, label='Load Actual')[0],
    'rpm': ax2.plot([], [], 'y-', lw=2, label='RPM')[0],
    'head_temp': ax1.plot([], [], 'c-', lw=2, label='Head temp')[0],
    'manifold_temp': ax1.plot([], [], 'm-', lw=2, label='Manifold temp')[0],
    'air_temp': ax1.plot([], [], 'k-', lw=2, label='Air temp')[0],
}

# Add legends for each axis
handles, labels = [], []
for key in lines:
    handles.append(lines[key])
    labels.append(lines[key].get_label())

# Create a single legend
ax1.legend(handles, labels, loc='upper left')

ax1.set_xlabel("Time")
ax1.set_ylabel("Percentage / Load / Temperature (°C)")
ax2.set_ylabel("RPM")

# Embed the plot into the window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=4, column=4, padx=10, pady=10)

def init_plot():
    ax1.set_ylim(0, 110)
    ax2.set_ylim(0, 22000)
    return list(lines.values())

TIME_WINDOW = 20 # seconds
MAX_MEASUREMENTS = TIME_WINDOW * 4 # one measurement every 250ms
def update_plot(frame):
    times = [measurement['millis'] for measurement in measurements[-MAX_MEASUREMENTS:]]

    for key in lines:
        ydata = [measurement[key] for measurement in measurements[-MAX_MEASUREMENTS:]]
        lines[key].set_xdata(times)
        lines[key].set_ydata(ydata)

    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    canvas.draw()
    return list(lines.values())

ani = animation.FuncAnimation(fig, update_plot, frames=range(10), init_func=init_plot, blit=True)



is_recording = False
log_file = None

def toggle_record():
    global is_recording, log_file

    if is_recording:
        is_recording = False
        if log_file:
            log_file.close()
            log_file = None
        record_button.config(text="Start Recording", bg="green")
    else:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/log_{current_time}.csv"
        log_file = open(filename, "w")
        print("millis,throttle,load_request,load_actual,rotations,rpm,head_temp,manifold_temp,air_temp", file=log_file)
        record_button.config(text="Stop Recording", bg="red")
        is_recording = True

record_button = tk.Button(window, text="Start Recording", bg="green", command=toggle_record, width=20, height=2, font=("Helvetica", 13, "bold"))
record_button.grid(column=3, row=6, padx=10, pady=10)

def toggle_serial():
    if ser.is_open:
        ser.close()
        button.config(text="Connect", bg="yellow")
    else:
        ser.port = 'COM3'
        ser.baudrate = 9600
        ser.open()
        button.config(text="Disconnect", bg="pink")

button = tk.Button(window, text="Connect", bg="yellow", command=toggle_serial, width=10, height=2, font=("Helvetica", 13, "bold"))
button.grid(column=0, row=9, padx=10, pady=10)


# Main Event Loop
def read_serial():
    while True:
        try:
            if ser.is_open and ser.in_waiting:
                line = ser.readline().decode('utf-8').rstrip()

                # If recording, write the line to the log file
                if is_recording and log_file:
                    print(line, file=log_file)

                # Print to GUI serial monitor
                serial_monitor.config(state=tk.NORMAL)
                serial_monitor.insert(tk.END, line + "\n")
                serial_monitor.yview(tk.END)
                serial_monitor.config(state=tk.DISABLED)
                
                # Extract individual data
                data = line.split(",")
                millis, throttle_percentage, load_requested, load_actual, rotations, rpm, temp1, temp2, temp3 = data

                measurement = {
                    'millis': float(millis),
                    'throttle_percentage': float(throttle_percentage),
                    'load_requested': float(load_requested),
                    'load_actual': float(load_actual) / 100,
                    'rotations': float(rotations),
                    'rpm': float(rpm),
                    'head_temp': float(temp1),
                    'manifold_temp': float(temp2),
                    'air_temp': float(temp3),
                }
                measurements.append(measurement)

                # Update GUI labels
                rpm_label.config(text=f"RPM: {rpm}")
                load_actual_label.config(text=f"Load mV: {load_actual}")
                temp1_label.config(text=f"Head Temp:{temp1}") 
                temp2_label.config(text=f"Manifold Temp:{temp2}") 
                temp3_label.config(text=f"Air Temp:{temp3}") 
        except serial.SerialException as e:
            print(f"Encounted an error: {e}. Continuing...")

# Function to handle the key press event
def STOP(event):
    kill_throttle()
    kill_load()

def STOPLOAD(event):
    kill_load()

def corner_test(event):
    throttle100()
    threading.Timer(1, throttle50).start()  # Delay for 1 second
    threading.Timer(1.5, throttle100).start()  # Delay for 2 seconds from start

def quick_connect(event):
    toggle_serial()

# Bind keys to above function
root.bind('<Control-x>', STOP)
root.bind('<Control-r>', corner_test)
root.bind('<Control-c>', quick_connect)
root.bind('<Control-l>', STOPLOAD)

thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

window.mainloop()
