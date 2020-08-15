document.getElementById("post0").className = 'big-image card';
var myVar = setInterval(myTimer, 5000);

function search_check(){
	document.getElementById("search_btn").setAttribute('type', 'submit')
	if (document.getElementById("search_input").value == '' || document.getElementById("search_input").value == ' '){
		document.getElementById("search_btn").setAttribute('type', 'button')
	}
}

function myTimer() {
    next_big_image(document.querySelector('div.big-image:not(.hide)').id.slice(-1));
}

function visible_big_image_change(current_big_image_index){
	document.getElementById('previous_big_image' + String(current_big_image_index)).className = 'hide-on-med-and-down';
	document.getElementById('next_big_image' + String(current_big_image_index)).className = 'hide-on-med-and-down';
}

function hidden_big_image_change(current_big_image_index){
	document.getElementById('previous_big_image' + String(current_big_image_index)).className = 'hide-on-med-and-down hide';
	document.getElementById('next_big_image' + String(current_big_image_index)).className = 'hide-on-med-and-down hide';
}

function previous_big_image(current_big_image_index){
	reset_interval();
	document.getElementById('post' + String(current_big_image_index)).className = 'big-image card hide';
	if (current_big_image_index == 0){
		post4.className = 'big-image card visible';
	}
	else {
		document.getElementById('post' + String(Number(current_big_image_index) - 1)).className = 'big-image card visible';
	}
}

function next_big_image(current_big_image_index){
	reset_interval();
	document.getElementById('post' + String(current_big_image_index)).className = 'big-image card hide';
	if (current_big_image_index == 4){
		post0.className = 'big-image card visible';
	}
	else {
		document.getElementById('post' + String(Number(current_big_image_index) + 1)).className = 'big-image card visible';
	}
}

function reset_interval(){
	window.clearInterval(myVar);
	myVar = setInterval(myTimer, 5000);
}