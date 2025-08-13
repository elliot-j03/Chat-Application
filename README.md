# Desktop Chat Application
A simple chat application that allows users to communicate with each other through text-based messaging. The use of websockets allows for real-time updates for all clients connected to the server. The **server.py** script is used for running and shutting down the server, and the **client.py** script is used to handle the client's gui.<br>

### Tag System
In order to deal with the many requests that users need to make across the app, I implemented a custom tag system. Each request sends an identifying tag in the form of **"\<_\>"**, replacing **"\_"** with the corresponding letter. Each request comes from the client's GUI components, which is then sent to **server.py** to be handled and sent back to **base_window.py**, resulting in a change on client side. The path of each is explained on **tags.txt** in the repository.<br>

### Account Requests
To chat, users will need to login or create an account. During these processes, user input is checked against an existing file-based storage that holds user data. If login or account creation succeeds, the user will be logged in or have their new credentials added to the user data file. If it fails, an error message will occur explaining what went wrong with the request.<br>

### Chatting
When chatting, users will type their message into the input box at the bottom of the window. When sent, the message will be sent to the server and added to the chat log file. This is updated and then returned to all clients connected to the server. This chat log is loaded in full when users log in. In the chat log file, the name of each user is marked with a preceding "!" which is used on the client side to identify which words to make bold.
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
git clone https://github.com/elliot-j03/Chat-Application.git
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
Now you should be set up correctly and able to run the chat application.
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
