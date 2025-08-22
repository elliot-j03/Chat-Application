# Desktop Chat Application
A simple chat application that allows users to communicate with each other through text-based messaging. The use of websockets allows for real-time updates for all clients connected to the server. The **server.py** script is used for running and shutting down the server, and the **client.py** script is used to handle the client's gui. My aim in this project was not to create an amazing looking gui, but to practice and improve my programming skills.<br>

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
### The Client
The client logs in and sends chats:<br>

<img src="https://github.com/user-attachments/assets/369dd940-ad3c-4913-a478-b186c82bd3da" alt="Log in and Chat" width="800"/>

Multiple clients chat and one leaves, updating the list of online users:<br>

<img src="https://github.com/user-attachments/assets/d7b04aa7-8f5a-482a-9720-4d6a863d82aa" alt="Multiple clients" width="800"/>

The client creating a new account:<br>

<img src="https://github.com/user-attachments/assets/12651ef9-1058-4655-81fa-14d90900d520" alt="New user" width="800"/>


The client tries and fails to connect:<br>

<img src="https://github.com/user-attachments/assets/53b46015-ebe6-45a7-8585-e60a17f6e9d2" alt="Cant Connect" width="800"/>

### The Server
The server gui, controls if the server is running and shows a log of the server activity:<br>

<img width="800" alt="Screenshot 2025-08-22 234443" src="https://github.com/user-attachments/assets/07945c17-bea3-4179-a95f-04f44392b84d" />

## Set-Up
### To try this code out for yourself, please follow the steps below...
First of all, make sure you have python installed on your system. If not, you can get it here on the [official website](https://www.python.org/downloads/) <br>

Next, copy the code from this repository into your own editor, or alternatively clone the repository into whichever directory your using with the git clone command
```console
git clone https://github.com/elliot-j03/Chat-Application.git
```
If you haven't already got a .venv file in your directory, run this command to create a new one
```console
python -m venv .venv
```
Then, install the required modules. To do this you need to activate the python virtual environment
```console
source .venv/Scripts/activate
```
and use pip to download what you need
```console
pip install -r requirements.txt
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
