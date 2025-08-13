# Desktop Chat Application
Stuff
## Libraries
* Socket
* Tkinter
* TTKBootstrap
* PIL
## Preview
gifs
## Set-Up
### To try this code out for yourself, please follow the steps below...
First of all, make sure you have python installed on your system. If not, you can get it here on the [official website](https://www.python.org/downloads/) <br>

Next, copy the code from this repository into your own editor, or alternatively clone the repository into whichever directory your using with the git clone command
```console
git clone https://github.com/elliot-j03/Miniature-Engine.git
```
If you havent already got a .venv file in your directory, run this command to create a new one
```console
python -m venv .venv
```
Then, install the required modules. To do this you need to activate the python virtual environment
```console
source .venv/Scripts/activate
```
and use pip to download what you need
```console
pip install -r requirement.txt
```
Now you should be set up correctly and able to run the mini engine.
For the chat application to work, you need to run both **server.py** and **client.py**. You can do this by either running them in your editor or using the terminal as shown below. If you're 
using the terminal, please open two separate terminals and virtual environments for each script. You **DO NOT** need to install the modules again.<br>
### Terminal 1:
```console
source .venv/Scripts/activate
python path/to/server.py
```
### Terminal 2:
```console
source .venv/Scripts/activate
python path/to/client.py
```
If you want more than one client running (which you probably will), you can simply open another terminal for the second **client.py**
