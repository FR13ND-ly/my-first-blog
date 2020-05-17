function makevisibleusermenu(){
    var usermenu = document.getElementById('usermenu');
    if (usermenu.className == 'row pinned hide'){
        usermenu.className = 'row pinned ';
    }
    else{
        usermenu.className = 'row pinned hide';
    }
}