HI 

First project of this scale, so I'm sorry if I'm missing key infomration. Ask and I will hapily answer any questions.

This is the Arduino code and Python program for controlling my mini dyno setup for testing small nitro engines (3.5cc-15cc). 


The setup is:
Arduino UNO R4 Minima for receiving all the data to be outputted over serial
a 3.5AHB eddy current break
hall effect sensor for measuring RPM
controlling the load on the break with a 0-5v signal.
and using a 200mV connection 2A shunt to measure the load being applied.
3x temp sensors using Onewire
2x servos to control Throttle and mixture on the engine **(current issue with the servos jitering, on a seperate power supply with common grounds, any help appreciated)**
I then have a GUI for conterolling all this and outputting a graph of the data live, and logging for all the data coming from the arduino over serial.

**Current issues:**

-The servos jiter, they are on a seperate power supply with common grounds

-I have a keybind setup for the throttle to go from 100% down to 50% breifly then back to 100% (referred to a s a "Run" from now on(CTRL+R)) (simulating the engines being throttled for a corner during a race).
I need to be able to identify this period of time in the data being recorded. 
My thoguhts were to add an aditional output to the log file called, somthing like "Runs" which starts at 0, and increments each time the run command is perfomred, but only outputs the incremented number when the run command is started, and finishes when the rpm reaches it's peak for 3 seconds. 
From this I can identify the incrementing number and pull out the Runs from the data easily in Excel. 

-I would like to be able to have a list of differnt "Runs" to choose from but that's not key at this time.

-This has mostly been coded by a friend who's been invaluable, and my occasional addition with the help of ChatGPT, so I apologise for any lack of understanding on my part. 

Thanks for reading and checking out the project, any input is appreciated :)
