import random
import re
import urllib.parse

from datetime import timedelta
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# Configure session to use filesystem
app.config["SECRET_KEY"] = "bd82J0_aQhsVR04$:1MmNxTNsQ"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=16)
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

# Index
@app.route("/")
def index():
    current_user = session['username'] if "username" in session else None
    previous_chat = session['chatroom'] if 'chatroom' in session else None
    return render_template("index.html", public_chatrooms=chatrooms, text=text, previous_chat=previous_chat, online_user=current_user)

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
                while len(local_messages) > 5:
                    stored_messages.remove(local_messages[0])
                    local_messages.remove(local_messages[0])
        if check:
            print(local_messages)
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
        chatcode = code(12)
        newchat = {'code': chatcode, 'name': request.form.get('chatroom'), 'type': request.form.get('room_type')}
        chatrooms.append(newchat)
        return redirect(f"/{newchat['name']}/{newchat['code']}")

@app.route("/login", methods=["POST"])
def login():
    current_user = session['username'] if "username" in session else None
    previous_chat = session['chatroom'] if 'chatroom' in session else None
    username = request.form.get("username")
    if len(username) < 1:
        text = "No puede ingresar un usuario vacío."
    elif username in online_users:
        text = "Ese nombre ya se encuentra conectado."
    else:
        session['username'] = username
        online_users.append(username)
        text = f"Has iniciado sesión como {username}."
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

@socketio.on("send message")
def send_message(data):
    data['message'] = data['message'].strip()
    print(data)
    if len(data["message"]) > 0:
        message = {'chatroom': data['chatroom'], 'author': session['username'], 'message': urllib.parse.unquote_plus(data['message'])}
        print(message)
        stored_messages.append(message)
        local_messages.append(message)
        emit("broadcast message", {'message': message}, broadcast=True)

@socketio.on("submit login")
def user(data):
    user_login = data["username"]
    if len(user_login) > 0 and user_login not in online_users:
        emit("announce login", {'user_login': user_login}, broadcast=True)