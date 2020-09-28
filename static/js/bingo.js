document.addEventListener('DOMContentLoaded', () => {
	var table = document.querySelector('.ticket');
	try {if (table.rows.length > 0)
		document.querySelector('#ticketgen').disabled = true;
		refresh()
	}
	catch {};
	function refresh() {
		all = document.querySelectorAll('#ticket td');
		for (i = 0; i < all.length; i++) {
			arr = document.querySelector('#drawed').innerHTML
			if (arr.includes(all[i].innerHTML)) {
				all[i].setAttribute("class","drawn");
			};
		};
	};
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('#ticketgen').onclick = () => {
			const user = document.getElementById('current_user').innerHTML;
			socket.emit('generate ticket', {'name': user});
		};
		document.querySelector('#draw').onclick = () => {
		socket.emit('draw number', {'newgame': true})
		};
	});
	socket.on('return ticket', data => {
		var ticket = {'name': data['name'], 'score': data['score'], 'top': data['top'], 'mid': data['mid'], 'bot': data['bot']},
		table = document.createElement('table'),
		name = document.createElement('tr'),
		top = document.createElement('tr'),
		mid = document.createElement('tr'),
		bot = document.createElement('tr');
		name.innerHTML = '<th colspan="3">' + ticket['name'] + '</th><th colspan="2">' + ticket['score'] + '</th>';
		var text = "";
		for (number in ticket['top']) {
			text += '<td class="undrawn">' + ticket['top'][number] + '</td>';
		};
		top.innerHTML = text
		var text = "";
		for (number in ticket['mid']) {
			text += '<td class="undrawn">' + ticket['mid'][number] + '</td>';
		};
		mid.innerHTML = text;
		var text = "";
		for (number in ticket['bot']) {
			text += '<td class="undrawn">' + ticket['bot'][number] + '</td>';
		};
		bot.innerHTML = text;
		document.querySelector('#ticket').appendChild(table);
		table.appendChild(name);
		table.appendChild(top);
		table.appendChild(mid);
		table.appendChild(bot);
		document.querySelector('#ticketgen').disabled = true;
	});
	socket.on('draw result', data => {
		document.querySelector('#drawed').innerHTML = data['drawed numbers'];
		for (i in data['tickets']) {
			if (data['tickets'][i]['name'] == document.getElementById('current_user').innerHTML) {
				document.querySelector('tr').innerHTML = '<th colspan="3">' + data['tickets'][i]['name'] + '</th><th colspan="2">' + data['tickets'][i]['score'] + '</th>';
			};
		};
		refresh()
	});
});