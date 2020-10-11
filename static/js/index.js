document.addEventListener('DOMContentLoaded', () => {
	function encode_utf8(s) {
		return encodeURIComponent(s);
	}
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelectorAll('.chatroom_link').forEach(link => {
			link.onclick = () => {
				const username = encode_utf8(document.getElementById('current_user').innerHTML);
				var code = link.href
				code = code.split([`${link.innerHTML}/`]);
				code = code[1]
		        socket.emit('submit login', {'username': username, 'chatroom': {'name': link.innerHTML, 'code': code}, 'type': 'announcement', 'message': `User ${username} has logged in` });
			};
	    });
	});
});