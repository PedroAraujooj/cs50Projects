function opennav() {
	var x = document.getElementById("nav");
	if (x.className === "nav") {
		x.className += " menujs";
		document.getElementById("linhas"). innerHTML= "&#10005;";	
	}
	else{
		x.className = "nav";
		document.getElementById("linhas"). innerHTML= "&#9776;";
	}
}
//&#10005;