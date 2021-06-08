var loadFile = function(event) {
	var image = document.getElementById('output');
    image.style.display="block"
	image.src = URL.createObjectURL(event.target.files[0]);
	var name = document.getElementById('nameImage');
	name.innerHTML = "asdaf";
};