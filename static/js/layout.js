if (!localStorage.getItem('red')) localStorage.setItem(('red'), "ff");
if (!localStorage.getItem('green')) localStorage.setItem(('green'), "ff");
if (!localStorage.getItem('blue')) localStorage.setItem(('blue'), "ff");

document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('body').style.backgroundColor = `#${localStorage.getItem('red')}${localStorage.getItem('green')}${localStorage.getItem('blue')}`
	document.querySelector('#red').placeholder = parseInt(localStorage.getItem('red'), 16)
	document.querySelector('#green').placeholder = parseInt(localStorage.getItem('green'), 16)
	document.querySelector('#blue').placeholder = parseInt(localStorage.getItem('blue'), 16)
	document.querySelector('#background').onsubmit = () => {
		var red = (Number(document.querySelector('#red').value).toString(16)).padStart(2,'0');
		var green = (Number(document.querySelector('#green').value).toString(16)).padStart(2,'0');
		var blue = (Number(document.querySelector('#blue').value).toString(16)).padStart(2,'0');
		localStorage.setItem(('red'), red);
		localStorage.setItem(('green'), green);
		localStorage.setItem(('blue'), blue);
		document.querySelector('body').style.backgroundColor = `#${localStorage.getItem('red')}${localStorage.getItem('green')}${localStorage.getItem('blue')}`;
		document.querySelector('#red').placeholder = parseInt(localStorage.getItem('red'), 16);
		document.querySelector('#green').placeholder = parseInt(localStorage.getItem('green'), 16);
		document.querySelector('#blue').placeholder = parseInt(localStorage.getItem('blue'), 16);
		return false;
	};
});