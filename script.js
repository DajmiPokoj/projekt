function handleSubmit(e) {
	e.preventDefault();
	const form = document.getElementById("form")
	const ves = form.querySelector("textarea").value;
	const width = document.querySelector("div:nth-child(2)").clientWidth; 
	const formular = new URLSearchParams(); 
	formular.append('ves', ves);
	formular.append('width', width);

	const url = form.action; 
	const method = form.method; 
	fetch(url, {method: method, body: formular})
		.then((res) => res.blob())
		.then((image) => {
			document.querySelector("#output").src = URL.createObjectURL(image);
			document.getElementById("output").style.visibility = "visible";
		})
}

function clear(e) {
    e.preventDefault();
    document.querySelector("textarea").value = "VES v1.6 600 400";
    document.getElementById("output").style.visibility = "hidden"; 
}