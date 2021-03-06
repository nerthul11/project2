import bingo
import datetime
import random
import re
import urllib.parse

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# Configure session to use filesystem
app.config["SECRET_KEY"] = "bd82J0_aQhsVR04$:1MmNxTNsQ"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=16)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

# Defining global variables
text = "" # Displays various texts
online_users = [] # List of online users
current_user = None # Used when rendering session['username'] to avoid KeyErrors.
chatrooms = [] # List of chatrooms
stored_messages = [] # All stored messages
local_messages = [] # Messages for the current chatroom

# Non-route functions
def code(length):
    pw_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    pw_chars = list(pw_chars)
    random.shuffle(pw_chars)
    pw = random.choices(pw_chars, k=length)
    pw = ''.join(pw)
    return pw

def validate(self):
    valid = re.fullmatch(r'[\w\s]+', self)
    return valid

# Index
@app.route("/")
def index():
    current_user = session['username'] if 'username' in session else None
    previous_chat = session['chatroom'] if 'chatroom' in session else None
    return render_template("index.html", public_chatrooms=chatrooms, text=text, previous_chat=previous_chat, online_user=current_user)

# Bingo
@app.route("/bingo")
def play_bingo():
    current_user = session['username'] if 'username' in session else None
    return render_template("bingo.html", tickets=bingo.tickets, online_user=current_user, drawed=bingo.drawed_numbers, info=bingo.info)

# Chatroom
@app.route("/<string:chatroom>/<string:code>", methods=["POST","GET"])
def chatroom(chatroom, code):
    current_user = session['username'] if 'username' in session else None
    url = {'code': code, 'name': chatroom}
    check = False
    if len(chatrooms) > 0:
        for i in chatrooms:
            if i['code'] == url['code'] and i['name'] == url['name']:
                check = True
                session['chatroom'] = {'code': i['code'], 'name': i['name']}
                local_messages.clear()
                for i in stored_messages:
                    if i['chatroom'] == session['chatroom']:
                        local_messages.append(i)
                while len(local_messages) > 100:
                    stored_messages.remove(local_messages[0])
                    local_messages.remove(local_messages[0])
        if check:
            return render_template("chatroom.html", chatroom=chatroom, code=code, online_user=current_user, messages=local_messages)
        else:
            return "PAGE NOT FOUND"
    else:
        return "NO CHATROOMS EXIST"

# Chat search: When you insert a code it tries to redirect you to a chatroom with that code.
@app.route("/search", methods=["POST"])
def chatsearch():
    check = request.form.get("code")
    valid_room = False
    for i in chatrooms:
        name = i['name']
        code = i['code']
        if check == code:
            valid_room = True
            return redirect(f"/{name}/{code}")
    if not valid_room:
        return "PAGE NOT FOUND"

@app.route("/create")
def create_chatroom():
    current_user = session['username'] if 'username' in session else None
    text = ""
    return render_template("create.html", text=text, online_user=current_user)

@app.route("/create/check", methods=["POST"])
def check():
    current_user = session['username'] if 'username' in session else None
    existent_chatroom = False
    for chatroom in chatrooms:
        if request.form.get('chatroom') == chatroom['name']:
            existent_chatroom = True
    if existent_chatroom:
        text = "Chatroom name already exists."
        return render_template("create.html", text=text, online_user=current_user)
    else:
        valid = validate(request.form.get('chatroom'))
        if valid:
            chatcode = code(12)
            newchat = {'code': chatcode, 'name': request.form.get('chatroom'), 'type': request.form.get('room_type')}
            chatrooms.append(newchat)
            return redirect(f"/{newchat['name']}/{newchat['code']}")
        else:
            text = "Chatroom name can only contain alphanumeric characters"
            return render_template("create.html", text=text, online_user=current_user)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    username = username.strip()
    if len(username) < 1:
        text = "Username can't be empty"
    elif not validate(username):
        text = "Only alphanumeric characters and whitespaces allowed"
    elif username in online_users:
        text = f"User '{username}' is already online"
    else:
        session['username'] = username
        online_users.append(username)
        text = f"Has iniciado sesión como {username}."
    current_user = session['username'] if "username" in session else None
    previous_chat = session['chatroom'] if 'chatroom' in session else None
    return render_template("index.html", public_chatrooms=chatrooms, text=text, online_user=current_user, previous_chat=previous_chat)

@app.route("/logout")
def logout():
    if "username" in session:
        try:
            online_users.remove(session['username'])
        except ValueError:
            pass
        session.pop("username",None)
        return "Logged out"
    else:
        return "Couldn't log out"

@socketio.on("draw number")
def drawnumber():
    bingo.draw_number()
    emit("draw result", {'drawed numbers': bingo.drawed_numbers, 'tickets': bingo.tickets, 'info': bingo.info}, broadcast=True)

@socketio.on("generate ticket")
def generate_ticket(data):
    ticket = bingo.generate_ticket(data['name'])
    bingo.tickets.append(ticket)
    emit("return ticket", ticket)

@socketio.on("send message")
def send_message(data):
    data['message'] = data['message'].strip()
    if len(data["message"]) > 0:
        time = datetime.datetime.now()
        timestr = time.strftime("%H:%M")
        message = {'chatroom': data['chatroom'], 'type': 'message', 'author': session['username'], 'message': urllib.parse.unquote_plus(data['message']), 'time': timestr}
        stored_messages.append(message)
        local_messages.append(message)
        emit("broadcast message", {'message': message}, broadcast=True)

@socketio.on("submit login")
def user(data):
    stored_messages.append(data)
    local_messages.append(data)
    print(stored_messages)
    emit("announce login", data, broadcast=True)