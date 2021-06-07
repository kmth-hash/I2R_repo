var loadFile = function(event) {
	var image = document.getElementById('output');
    image.style.display="block"
	image.src = URL.createObjectURL(event.target.files[0]);
	localStorage.setItem('img',URL.createObjectURL(event.target.files[0]))
};