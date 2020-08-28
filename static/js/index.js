document.addEventListener('DOMContentLoaded', () => {
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('#login').onsubmit = () => {
			const username = document.querySelector('#username').value;
			socket.emit('submit login', {'username': username});
		};
	});
	socket.on('announce login', data => {
		const li = document.createElement('li');
		li.innerHTML = `${data.user_login} ha iniciado sesión.`;
		document.querySelector('#global_message').append(li);
	});
});