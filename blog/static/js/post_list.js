post0.style.display = 'block';
post1.style.display = 'none';
post2.style.display = 'none';
post3.style.display = 'none';
post4.style.display = 'none';
next_big_image_btn = document.getElementById('next_big_image');
previous_big_image_btn = document.getElementById('previous_big_image');
function make_visible_tools_of_big_image(){
    next_big_image_btn.style.visibility = 'visible';
    previous_big_image_btn.style.visibility = 'visible';
}
function make_hidden_tools_of_big_image(){
    next_big_image_btn.style.visibility = 'hidden';
    previous_big_image_btn.style.visibility = 'hidden';
}
function previous_big_image(){
        alert(document.querySelector("div[class='big_image'][style='display:block']"));
        if (post0.style.display == 'block'){
            post0.style.display = 'none';
            post4.style.display = 'block';
        }
        else if (post1.style.display == 'block'){
            post1.style.display = 'none';
            post0.style.display = 'block';
        }
        else if (post2.style.display == 'block'){
            post2.style.display = 'none';
            post1.style.display = 'block';
        }
        else if (post3.style.display == 'block'){
            post3.style.display = 'none';
            post2.style.display = 'block';
        }
        else if (post4.style.display == 'block'){
            post4.style.display = 'none';
            post3.style.display = 'block';
        }
    }
    function next_big_image(){
        if (post0.style.display == 'block'){
            post0.style.display = 'none';
            post1.style.display = 'block';
        }
        else if (post1.style.display == 'block'){
            post1.style.display = 'none';
            post2.style.display = 'block';
        }
         else if (post2.style.display == 'block'){
            post2.style.display = 'none';
            post3.style.display = 'block';
        }
        else if (post3.style.display == 'block'){
            post3.style.display = 'none';
            post4.style.display = 'block';
        }
        else if (post4.style.display == 'block'){
            post4.style.display = 'none';
            post0.style.display = 'block';
        }
            
    }