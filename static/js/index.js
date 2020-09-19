document.addEventListener('DOMContentLoaded', () => {
	function encode_utf8(s) {
		return encodeURIComponent(s);
	}
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('.chatroom_link').onclick = () => {
			const username = encode_utf8(document.querySelector('#username').value);
			socket.emit('submit login', {'username': username});
		};
	});
	socket.on('announce login', data => {
		const li = document.createElement('li');
		li.innerHTML = `${data.user_login} ha iniciado sesión.`;
		document.querySelector('#global_message').append(li);
	});
});