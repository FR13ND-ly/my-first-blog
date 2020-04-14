function makevisibleusermenu(){
    var usermenu = document.getElementById('usermenu');
    if (usermenu.style.display != 'none'){
        usermenu.style.display = 'none';
    }
    else{
        usermenu.style.display = 'block';
    }
}