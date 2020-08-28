document.addEventListener('DOMContentLoaded', () => {
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('#send').onclick = () => {
			const message = document.querySelector('#message').value;
			socket.emit('send message', {'chatroom': {'code':document.querySelector('#code').innerHTML, 'name': document.querySelector('#chatroom').innerHTML}, 'message': message});
		};
	});
	socket.on('broadcast message', data => {
		if (data.message['chatroom']['code'] == document.querySelector('#code').innerHTML) {
			const li = document.createElement('li');
			li.innerHTML = `${data.message['author']} dice: ${data.message['message']}`;
			document.querySelector('#messages').append(li);
			var listlen = document.getElementById('messages').getElementsByTagName('li').length;
			while (listlen > 100) {
				var list = document.getElementById('messages');
				list.removeChild(list.childNodes[0]);
				var listlen = document.getElementById('messages').getElementsByTagName('li').length;
			};
		};
	});
});