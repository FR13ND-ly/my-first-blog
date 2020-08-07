document.title = "Înregistrare";
password_input = document.getElementById("password1");
repeated_password_input = document.getElementById("password2");

password_input.onblur = function(){
	if ((password_input.value).length < 5 ){
		password_input.className = "validate invalid";
	} 
	else {
		password_input.className = "validate valid";
	if (repeated_password_input.value == password_input.value){
		repeated_password_input.className = "validate valid";
	}
	}
}

repeated_password_input.onblur = function(){
	if (repeated_password_input.value != password_input.value){
		repeated_password_input.className = "validate invalid";
	}
	else {
		if ((password_input.value).length < 5 ){
			repeated_password_input.className = "validate valid";
		}
	}
}