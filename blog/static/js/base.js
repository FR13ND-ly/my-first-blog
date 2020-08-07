function show_mobile_usermenu(){
    var mobile_menu = document.getElementById('mobile_menu');
    if (mobile_menu.className == 'row pinned hide hide-on-med-and-up'){
        mobile_menu.className = 'row pinned hide-on-med-and-up';
    }
    else{
        mobile_menu.className = 'row pinned hide hide-on-med-and-up';
    }
  }

function makevisibleusermenu(){
    var usermenu = document.getElementById('usermenu');
    if (usermenu.className == 'row pinned hide'){
        usermenu.className = 'row pinned visible_usermenu';
    }
    else{
        usermenu.className = 'row pinned hide';
    }
}