# IOT Cloud Weather Station With Raspberry pi 4 Model B
## Abstract
<p> The purpose of this Weather Station is to provide real time weather information to the user on demand. The weather station consists of Sensors capable of reading temperature, pressure, humidity, etc. These details are sent to a Thingspeak Server that is hosted in a remote location. 

The existing system gets the data from sencors and sends it to the remote server. this project takes the reading from the physical environment.</p>

## Components
<ol>
  <li> Raspberry Pi 4 Model B </li>
  <li> Breadboard </li>
  <li> Connecting wires </li>
  <li> DHT11 Digital Humidity and Temperature Sensor </li>
  <li> BMP180 Sensor </li>
  <li> Power Source for Raspberry Pi </li>
  <li> An ethernet cable or a Wifi Module [USB ones work fine] </li>
</ol>

## Requirements
<ul>
  <li> Router with DHCP capability</li>
  <li> Wired or wireless Router </li>
  <li> Android Phone / PC / Laptop </li>
</ul>

## Circuit Diagram
![diagram](https://user-images.githubusercontent.com/68354042/144743086-37825040-04f5-495e-974e-d2c751e7658c.jpg)

## Pre Connection Procedure
<ol>
  <li> Flash the <a href="https://www.raspberrypi.org/downloads/raspbian/">Raspbian OS</a> into the MicroSD card of your Raspberry Pi using the <a href="https://www.raspberrypi.com/software/">Raspberry Pi Imager</a> Software</li>
  <li> Insert the MicrSD card into your Rapsberry Pi </li>
  <li> Download and run <a href="http://www.putty.org/"> Putty</a>, a SSH Client, or windows Powershell.
  <li> Power up the Raspberry Pi and connect it to your router using an ethernet cable / Wifi</li>
  <li> Determine the IP Address of your Raspberry pi from the router and enter that IP Address as hostname in the Hostname text field in putty / Powershell</li>
  <li> Connect to the Pi using putty / Powershell, even if the connection refuses once or twice, its okay, try again, it will connect. </li>
  <li> The default username is "pi" and password is "raspberry" by dafult, login to your pi using these credentials </li>
  <li> Expand the file system  in Raspberry pi <code>sudo raspi-config</code> </li>
  <li> Set the time zone of the system in Raspberry pi <code>sudo raspi-config</code></li>
  <li> Run the udpate a few times <code>sudo apt-get update</code> </li>
  <li> Install the necessary softwares <code>sudo apt-get install git-core python3-dev python-pip python-smbus</code> .These will come in handy later </li>
  <li> Then reboot, <code>sudo reboot</code> </li>
</ol>

## Preparing the Pi for DHT11
<ol>
  <li> Connect the sensor to the Pi as shown in the circuit diagram </li>
  <li> <code>git clone https://github.com/adafruit/Adafruit_CircuitPython_DHT.git</code> to clone the Adafruit_CircuitPython_DHT repository into your Pi</li>
  <li> <code>cd Adafruit_CircuitPython_DHT</code> </li>
  <li> <code>sudo apt-get install build-essential python3-dev python-openssl</code> to install the necessary packages needed to install external python libraries</li>
  <li> <code>sudo python3 setup.py install</code> to install the external library</li>
  <li><code>cd examples</code></li>
  <li> <code>sudo ./AdafruitDHT.py 2302 4</code> to run the example and check if the sensor is working or not</li>
  <li>The simplest way to install install via pip3 <code>pip install adafruit-circuitpython-dht</code> </li>
</ol>

## Preparing the Pi for BMP180 / BMP085
![i2c](https://user-images.githubusercontent.com/68354042/144743402-6e90e672-d6ff-44d1-b422-e0f7153e99ec.jpg)
<ol>
  <li> Connect the sensor to the Pi as shown in the circuit diagram </li>
  <li> The BMP Sernsors use I2C Communication Interface to communicate with the Raspberry Pi </li>
  <code> sudo apt-get install python-smbus</code><br>
  <code> sudo apt-get install i2c-tools</code>
  <li> Run <code>sudo raspi-config</code> and follow the prompts to install i2c support for the ARM core and linux kernel</li>
  <li> Then reboot, <code>sudo reboot</code> </li>
  <li> When you are done,run
  <br> <code>sudo i2cdetect -y 1</code> (if you are using a version 2 Raspberry Pi)<br> Once you give this , an address should show up the output <br><br><b> Before plugging in the sensor you will see -- every where.But After plug in you will see like the picture below:</b></li>
  <li> Install the Adafruit Python Library <br>
  <br> <code>sudo apt-get update</code> 
  <br> <code>sudo apt-get install git build-essential python-dev python-smbus</code> 
  <br> <code>git clone https://github.com/adafruit/Adafruit_Python_BMP.git</code> 
  <br> <code>cd Adafruit_Python_BMP</code> 
  <br> <code>sudo python setup.py install</code> </li>
  <li> Once the installation is complete <br> <code>cd examples</code> <br>
  <code>sudo python simpletest.py</code><br> To check whether or not the sensor is working </li>
</ol>



## The Python Script
The python script Weather Station.py is the main script that runs in the python to send the data to the database, it recieves the data from the sensors and sends it to a php file in the server via HTTP GET.
<br>
One more thing you need to do is to ensure that this code runs periodically as this code only sends data once, use <a href= "https://www.raspberrypi.org/documentation/linux/usage/cron.md">crontab</a> to automate this task. I would reccomend running this code for once in 15 or 30 minutes, any less will result in a very huge database with hardly an variation between neighbouring records. <br>
You need to modify the path in WeatherStation.py as per your server. You can run a local server in your raspberry pi and make it handle all the request.

## ThinkSpeak server
Goto Thinkspeak and signup. You can see channel upleft.Create one.You can see a Heading option API KEY.Copy and paste it on your project field 'key'.
![Thingspeak](https://user-images.githubusercontent.com/68354042/144743118-89b79245-c1d0-47a9-819f-8c2cb3d00561.jpg)


## Uses
Simply run:<br><code>python3 station.py</code><br>

## Systemless run
To run a program on your Raspberry Pi at startup is to modify the .bashrc  file. With the .bashrc method, your python program will run when you log in (which happens automatically when you boot up and go directly to the desktop) and also every time when a new terminal is opened, or when a new SSH connection is made. Put your command at the bottom of ‘/home/pi/.bashrc’. The program can be aborted with ‘ctrl-c’ while it is running!
<br><code>sudo nano /home/pi/.bashrc</code>
<br>Go to the last line of the script and add:<br>
<code>echo Running at boot 
sudo python3 /home/pi/your program file loaction</code><br>
Now reboot the Pi to hear the Pi speak at startup
<code>sudo reboot</code>
