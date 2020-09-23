document.addEventListener('DOMContentLoaded', () => {
	var table = document.querySelector('.ticket');
	try {if (table.rows.length > 0)
		document.querySelector('#ticketgen').disabled = true;
	}
	catch {};
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		document.querySelector('#ticketgen').onclick = () => {
			const user = document.getElementById('current_user').innerHTML;
			socket.emit('generate ticket', {'name': user});
		};
	});
	socket.on('return ticket', data => {
		var ticket = {'name': data['name'], 'top': data['top'], 'mid': data['mid'], 'bot': data['bot']},
		table = document.createElement('table'),
		name = document.createElement('tr'),
		top = document.createElement('tr'),
		mid = document.createElement('tr'),
		bot = document.createElement('tr');
		name.setAttribute("class","name");
		top.setAttribute("class","top");
		mid.setAttribute("class","mid");
		bot.setAttribute("class","bot");
		name.innerHTML = '<th>' + ticket['name'] + '</th>';
		var text = "";
		for (number in ticket['top']) {
			text += '<td>' + ticket['top'][number] + '</td>';
		};
		top.innerHTML = text
		var text = "";
		for (number in ticket['mid']) {
			text += '<td>' + ticket['mid'][number] + '</td>';
		};
		mid.innerHTML = text;
		var text = "";
		for (number in ticket['bot']) {
			text += '<td>' + ticket['bot'][number] + '</td>';
		};
		bot.innerHTML = text;
		document.querySelector('#ticket').appendChild(table);
		table.appendChild(name);
		table.appendChild(top);
		table.appendChild(mid);
		table.appendChild(bot);
		document.querySelector('#ticketgen').disabled = true;
	});
});