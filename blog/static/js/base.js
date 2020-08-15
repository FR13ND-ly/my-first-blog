$(".button-collapse").sideNav();
$('.collapsible').collapsible();
keyCodes = [65, 87, 69, 83, 79, 77, 69]
iteration = 0
addEventListener('keydown', function(e){
    if (e.keyCode == keyCodes[iteration]){
        iteration = iteration + 1;
        if (iteration == 7){
            document.getElementById('e-c').className = "brand-logo center rainbow"
        }
    }
    else {
        iteration = 0
    }
})