document.addEventListener('DOMContentLoaded', () => {
	function encode_utf8(s) {
		return encodeURIComponent(s);
	}
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('#send').onclick = () => {
			const message = encode_utf8(document.querySelector('#message').value);
			socket.emit('send message', {'chatroom': {'code':document.querySelector('#code').innerHTML, 'name': document.querySelector('#chatroom').innerHTML}, 'message': message});
			document.querySelector('#message').value = null;
		};
	});
	socket.on('broadcast message', data => {
		if (data.message['chatroom']['code'] == document.querySelector('#code').innerHTML) {
			var msgbox = document.createElement('div'), 
			msg = document.createElement('div'),
			p = document.createElement('p'),
			time = document.createElement('span');
			time.setAttribute("class","time_date");
			time.innerHTML = data.message['time'];
			if (data.message['author'] == document.getElementById('current_user').innerHTML) {
				msgbox.setAttribute("class","outgoing_msg")
				msg.setAttribute("class","sent_msg");
				p.innerHTML = data.message['message'];
			} else {
				msgbox.setAttribute("class","incoming_msg")
				msg.setAttribute("class","received_msg");
				p.innerHTML = `<strong>${data.message['author']}</strong><br> ${data.message['message']}`;
			};
			document.querySelector('.msg_history').appendChild(msgbox);
			msgbox.appendChild(msg);
			msg.appendChild(p);
			msg.appendChild(time);
			var listlen = document.querySelector('.msg_history').querySelectorAll('.msg_history > div').length;
			while (listlen > 100) {
				var msglist = document.querySelector('.msg_history');
				msglist.removeChild(msglist.childNodes[0]);
				var listlen = document.querySelector('.msg_history').querySelectorAll('.msg_history > div').length;
			};
		};
	});
	socket.on('announce login', data => {
       console.log("Socket received");
	});
});