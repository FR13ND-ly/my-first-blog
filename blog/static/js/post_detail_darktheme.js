document.title = document.getElementById("article_title").innerHTML;
var header = document.getElementsByTagName("head")[0];
var meta_description = document.createElement('meta');
meta_description.setAttribute('property', 'og:description');
meta_description.content = document.getElementById("post_text").innerHTML.substring(0, 41);
var meta_title = document.createElement('meta');
meta_title.setAttribute('property', 'og:title');
meta_title.content = document.getElementById("article_title").innerHTML;
var meta_type = document.createElement('meta');
meta_type.setAttribute('property', 'og:type');
meta_type.content = 'article';
header.appendChild(meta_description);
header.appendChild(meta_title);
header.appendChild(meta_type); 

function add_like(){ 
    like_icon = document.getElementById('like_icon');
    like_count = document.getElementById('like_count');
    input = document.getElementById('liked')
    document.getElementById('submit_btn').click()
    if (like_icon.innerHTML == "favorite") {
        like_icon.innerHTML = 'favorite_border'
        like_count.innerHTML = Number(document.getElementById('like_count').innerHTML) - 1;
        console.log('like removed')
    }
    else {
        like_icon.innerHTML = 'favorite'
        like_count.innerHTML = Number(document.getElementById('like_count').innerHTML) + 1;
        console.log('like added')
    }
}

function add_comment(){
    var comment_form = document.getElementById('comment_form');
    var add_comment_btn = document.getElementById('add_comment');
    add_comment_btn.className = "btn center-align light-blue darken-2 hide";
    comment_form.className = "card blue-grey darken-3";
    console.log('add new comment section opened')
}

function select_one_variant(variant){
    variants = document.querySelectorAll('a[name="variant_container"]');
    for (i = 0; i<variants.length; i++){
        variants[i].className = "collection-item white-text blue-grey darken-3";
        document.querySelector('input[id="'+variants[i].id +'"]').setAttribute("name","none");
    }
    variant.className = "collection-item active light-blue darken-2 ";
    document.querySelector('input[id="'+variant.id +'"]').name = 'variant';
}

function select_multi_variant(variant) {
    variant_input = document.querySelector('input[id="'+variant.id +'"]');
    if (variant.className == "collection-item white-text blue-grey darken-3"){
        variant.className = "collection-item active light-blue darken-2";
        variant_input.name = 'variant';
    }
    else {
        variant.className = "collection-item white-text blue-grey darken-3";
        variant_input.setAttribute("name","none");
    }
}