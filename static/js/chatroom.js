document.addEventListener('DOMContentLoaded', () => {
	function encode_utf8(s) {
		return encodeURIComponent(s);
	}
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('#send').onclick = () => {
			const message = encode_utf8(document.querySelector('#message').value);
			socket.emit('send message', {'chatroom': {'code':document.querySelector('#code').innerHTML, 'name': document.querySelector('#chatroom').innerHTML}, 'message': message});
		};
	});
	socket.on('broadcast message', data => {
		if (data.message['chatroom']['code'] == document.querySelector('#code').innerHTML) {
			var msgbox = document.createElement('div'), 
			msg = document.createElement('div');
			msgbox.setAttribute("class","messagebox");
			if (data.message['author'] == document.getElementById('current_user').innerHTML) {
				msg.setAttribute("class","sent");
				msg.innerHTML = data.message['message'];
			} else {
				msg.setAttribute("class","received");
				msg.innerHTML = `<strong>${data.message['author']}</strong><br> ${data.message['message']}`;
			};
			document.querySelector('#messages').appendChild(msgbox);
			msgbox.appendChild(msg);
			var listlen = document.getElementById('messages').getElementsByTagName('div').length;
			while (listlen > 5) {
				var msglist = document.getElementById('messages');
				msglist.removeChild(msglist.childNodes[0]);
				var listlen = document.getElementById('messages').getElementsByTagName('div').length;
			};
		};
	});
	socket.on('announce login', data => {
		const login = document.createElement('div');
		login.innerHTML = `${data.user_login} has joined the chatroom.`;
		document.querySelector('#messages').append(login);
	});
});