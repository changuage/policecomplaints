/*
var race_form = document.getElementById("raceForm")
console.log(race_form)
function handleForm(event){
	var map = document.getElementById("map")
	event.preventDefault()
	map.src = "/static/Maps/" + race_form['race'].value + ".html"
	console.log(map)
}
race_form.addEventListener('submit',handleForm)
*/
function handleChange(event) {
	console.log(this)
	document.getElementById("racemap").src = "/static/Maps/" + this.value + ".html"
	//map.src = "/static/Maps/" + race_form['race'].value + ".html"
}
document.getElementById("raceForm")['race'].onchange = handleChange
//console.log(race_button.onchange)