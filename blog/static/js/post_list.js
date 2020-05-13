post0.className = 'big-image card';
document.getElementById
function visible_big_image_change(current_big_image_index){
	document.getElementById('previous_big_image' + String(current_big_image_index)).style.display = 'block';
	document.getElementById('next_big_image' + String(current_big_image_index)).style.display = 'block';
}

function hidden_big_image_change(current_big_image_index){
	document.getElementById('previous_big_image' + String(current_big_image_index)).style.display = 'none';
	document.getElementById('next_big_image' + String(current_big_image_index)).style.display = 'none';
}

function previous_big_image(current_big_image_index){
	document.getElementById('post' + String(current_big_image_index)).className = 'big-image card hidden';
	if (current_big_image_index == 0){
		post4.className = 'big-image card';
	}
	else {
		document.getElementById('post' + String(Number(current_big_image_index) - 1)).className = 'big-image card';
	}
}

function next_big_image(current_big_image_index){
    document.getElementById('post' + String(current_big_image_index)).className = 'big-image card hidden';
	if (current_big_image_index == 4){
		post0.className = 'big-image card';
	}
	else {
		document.getElementById('post' + String(Number(current_big_image_index) + 1)).className = 'big-image card';
	}
}
