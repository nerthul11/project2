document.addEventListener('DOMContentLoaded', () => {
	function encode_utf8(s) {
		return encodeURIComponent(s);
	}
	function sendmessage() {
		const username = encode_utf8(document.querySelector('#username').value);
		socket.emit('submit login', {'username': username});
	});
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('.chatroom_link').addEventListener("click", sendmessage) 
	});
});