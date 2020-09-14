var save_button = document.getElementById('save_post');
var iframe = document.getElementById('post_text');
var post_code = document.getElementById('post_code');
var code_or_visual_icon = document.getElementById('set_code_or_visual_icon');
var add_variant_button = document.getElementById('add_variant_button');
var survey_container = document.getElementById('survey_container');
var card_action = document.getElementById('card-action');
var variant_index = document.querySelectorAll('input[name="variant"]').length;
var post_code = document.getElementById('post_code');
var post_text = window.frames[0].document.getElementsByTagName("body")[0];
var iframe_head = window.frames[0].document.getElementsByTagName("head")[0];
var material_icons = document.createElement('link');
var materialize = document.createElement('link');
var materialize_script = document.createElement('script');
var poppins_font = document.createElement('link');
var add_img = document.getElementById('add_img');
var edit_img = document.getElementById('edit_img');
post_text.innerHTML = post_code.value;
window.frames[0].document.getElementsByTagName("body")[0].contentEditable = true;
img_size_selector = document.getElementById("img_size_selector");
img_title  = document.getElementById("image_title");
materialize_script.src = "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"
materialize.href = "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css";
material_icons.href = "https://fonts.googleapis.com/icon?family=Material+Icons";
poppins_font.href = "https://fonts.googleapis.com/css2?family=Poppins:wght@100;400&display=swap";
poppins_font.rel = "stylesheet";
materialize.rel = 'stylesheet';
material_icons.rel = 'stylesheet';
iframe_head.appendChild(material_icons);
iframe_head.appendChild(materialize);
iframe_head.appendChild(materialize_script);
iframe_head.appendChild(poppins_font);
width_container = document.getElementById('width_container');
height_container = document.getElementById('height_container');
post_text.style = "font-size:18px; padding:2px;";
post_code.value = document.createTextNode(post_text.innerHTML).wholeText;
images = post_text.querySelectorAll('img');
post_text.innerHTML = post_code.value;
for (i = 0; i<images.length; i++){
    images[i].addEventListener("click", function(e){create_img_tools(e.target.id)}, true)
}

document.getElementById('file-input').oninput = function(){
    document.getElementById('pre_added_img').src = URL.createObjectURL(document.getElementById('file-input').files[0])
}

$(document).ready(function () {
    setTimeout(function () {
    var kelle = $('.select-wrapper');
    $.each(kelle, function (i, t) {
        t.addEventListener('click', e => e.stopPropagation())
    });
}, 500)
});

$(document).ready(function() {
    $('select').material_select();
});
$(document).ready(function(){
    $('.modal').modal();
});

$('.chips').on('chip.add', function(e, chip){
    set_tag_list()
    console.log('new tag added')
});

$('.chips').on('chip.delete', function(e, chip){
    set_tag_list()
    console.log('tag removed')
});

function set_tag_list(){
    chips_list = document.querySelectorAll('.chips')
    tags_container = ""
    for (i=0; i<chips_list.length; i++ ){
        if (chips_list[i].textContent != 'close'){
            tags_container = tags_container + chips_list[i].textContent + ""
        }
    }
    document.getElementById('tags_container').value = tags_container
}
function select_image_visible() {
    document.getElementById("select_image_menu").className = "";
    document.getElementById("add_image_menu").className = "hide"
    document.getElementById("add_image").checked = false
}

function add_image_visible() {
    document.getElementById("select_image_menu").className = "hide";
    document.getElementById("add_image_menu").className = "";
    document.getElementById("add_image").checked = true
}

function select_image(variant) {
    to_select_variants = document.querySelectorAll('img[name="variant"]')
    for (i = 0; i < to_select_variants.length; i++){
        to_select_variants[i].className = "image"
    }
    variant.className = "image selected_variant"
    console.log('image selected')
}
function add_image_cover() {
    $('#modal1').modal('open')
    document.getElementById("add_cover_photo").className = "btn waves-effect waves-light"
    document.getElementById("new_image").className = "btn waves-effect waves-light hide"
}

function second_stage_add_cover_photo(){
    if (document.getElementById("add_image").checked ) {
        document.getElementById("cover_name").value = "blog/static/media/" + document.getElementById('file-input').files[0].name;
        document.getElementById("representative_cover_img").src = URL.createObjectURL(document.getElementById('file-input').files[0]);
        new_image_variant = document.createElement('img')
        new_image_variant.className = "image"
        new_image_variant.width = 210
        new_image_variant.height = 210
        new_image_variant.setAttribute("onclick", "select_image(this)")
        new_image_variant.setAttribute('name', 'variant')
        new_image_variant.src = URL.createObjectURL(document.getElementById('file-input').files[0])
        new_image_variant.id = "blog/media/blog/static/media/" + document.getElementById('file-input').files[0].name
        document.getElementById('image_list').appendChild(new_image_variant)
    }
    else {
        src_container = (document.querySelector("img[class='image selected_variant']").id.split("/"))
        document.getElementById("cover_name").value = "blog/static/media/" + src_container[src_container.length -1];
        document.getElementById("representative_cover_img").src = "/media/blog/static/media/" + src_container[src_container.length -1];
    }
    console.log('cover image added')
    $("#modal1").modal('close')
}
$('.modal').modal({
    ready: function(modal, trigger) {
        alert('sad');
    }
})

function set_save_button_text(draw){
    if (draw){
        save_button.innerHTML = 'Salvează';
        save_button.className = "btn red";
        console.log('set to draft')
    }
    else {
        save_button.innerHTML = "Publică";
        save_button.className = "btn";
        console.log('set to publish')
    }
}

function set_code_or_visual(value){
    if (value){
        post_code.className = 'text_input s12 z-depth-1 hoverable';
        iframe.className = 'hide text_input s12 z-depth-1 hoverable';
        code_or_visual_icon.innerHTML = 'title';
        console.log('viewing code part of post')
    }
    else {
        post_code.className = 'hide text_input s12 z-depth-1 hoverable';
        iframe.className = 'text_input s12 z-depth-1 hoverable';
        code_or_visual_icon.innerHTML = 'code';
        console.log('viewing visual part of post')
    }
}

function activate_survey(approved){
    if (approved){
        survey_container.className = '';
        card_action.className = "card-action";
        console.log('surveys activated')
    }
    else {
        survey_container.className = 'hide';
        card_action.className = "card-action hide";
        console.log('surveys disabled')
    }
}

function delete_variant(number){
    document.getElementById('variant_container'+number).remove();
    console.log('variant removed')
}

function add_variant(){
    var variant_container = document.createElement('div');
    variant_container.className = 'input-field';
    variant_container.id = 'variant_container' + String(variant_index);
    variant_container.setAttribute("name","variant_container");
    var variant_input = document.createElement('input');
    variant_input.id =  'variant_input' + String(variant_index);
    variant_input.type = 'text';
    variant_input.name = 'variant_of_survey';
    variant_input.style = 'width:97%';
    var variant_label = document.createElement('label');
    variant_label.htmlFor = 'variant_input' + String(variant_index);
    variant_label.innerHTML = 'Variantă';
    var variant_remove_button = document.createElement('i');
    variant_remove_button.className = "material-icons prefix teal-text";
    variant_remove_button.innerHTML = 'delete';
    variant_remove_button.id= variant_index;
    variant_remove_button.style = 'margin-top:2.5%; cursor:pointer';
    variant_remove_button.addEventListener('click', function(){delete_variant(this.id)});
    survey_container.insertAdjacentElement("beforeend", variant_container);
    variant_container.appendChild(variant_input);
    variant_container.appendChild(variant_label);
    variant_container.appendChild(variant_remove_button);
    variant_index = variant_index + 1;
    console.log('added new survey variant')
}

function size_change(){
    if(img_size_selector[img_size_selector.selectedIndex].value == 'custom'){
        width_container.className = "input-field col s6";
        height_container.className = "input-field col s6";
    }
    else {
        width_container.className = "input-field col s6 hide";
        height_container.className = "input-field col s6 hide";
    }
}

post_text.oninput = function(){
    post_code.value = document.createTextNode(post_text.innerHTML).wholeText;
    images = post_text.querySelectorAll('img');
    for (i = 0; i<images.length; i++){
        images[i].addEventListener("click", function(e){create_img_tools(e.target.id)},
            true)
    }
}
post_code.oninput =function(){
    post_text.innerHTML = post_code.value;
}

function first_stage_add_image(){
    if (document.getElementById("add_image").checked) {
        document.getElementById('representative-img').src = URL.createObjectURL(document.getElementById('file-input').files[0]);
        new_image_variant = document.createElement('img')
        new_image_variant.className = "image"
        new_image_variant.width = 210
        new_image_variant.height = 210
        new_image_variant.setAttribute("onclick", "select_image(this)")
        new_image_variant.setAttribute('name', 'variant')
        new_image_variant.src = URL.createObjectURL(document.getElementById('file-input').files[0])
        new_image_variant.id = "blog/media/blog/static/media/" + document.getElementById('file-input').files[0].name
        document.getElementById('image_list').appendChild(new_image_variant)
    }
    else {
        document.getElementById('representative-img').src = document.querySelector("img[class='image selected_variant']").src;
    }
    add_img.className = 'waves-effect waves-light btn green';
    edit_img.className = 'waves-effect waves-light btn green hide';
}
function reset_add_image_menu(){
    document.getElementById('pre_added_img').src = '';
    document.getElementById('representative-img').src = '';
    img_size_selector.selectedIndex = 1;
    size_change();
    img_title.value = '';
    $('#add_image_form').trigger("reset");
    document.querySelector('input[name="image_align"][value ="left"]').checked = true;
}

function second_stage_add_image(){
    if (document.getElementById("add_image").checked ) {
        img_name = document.getElementById('file-input').files[0].name;
    }
    else {
        src_container = (document.querySelector("img[class='image selected_variant']").id.split("/"))
        img_name = src_container[src_container.length -1];
    }
    if(img_size_selector[img_size_selector.selectedIndex].value != 'custom'){
        size = img_size_selector[img_size_selector.selectedIndex].value;
        code = "<img class='responsive-img materialboxed' title='" + img_title.value + "' data-caption='" + img_title.value + "' id='" + img_name + "' align='"+ document.querySelector('input[name="image_align"]:checked').value + "' style='position:relative; width:" + size + "%'  src='/media/blog/static/media/" + img_name + "'/>";
    }
    else{
        code = "<img style='position: relative;object-fit: cover; overflow: hidden;' class='materialboxed' title='" + img_title.value + "' data-caption='" + img_title.value + "'  id='" + img_name + "' title='" + img_title.value +"' align='"+ document.querySelector('input[name="image_align"]:checked').value + "' width='"+ document.getElementById('width_input').value + "' height='"+ document.getElementById('height_input').value+"' src='/media/blog/static/media/" + img_name + "'/>";
    }
    format('insertHTML', code);
    console.log('added image')
    reset_add_image_menu();
}

function remove_img_tools(img){
    window.frames[0].document.getElementById(img + 'tools_container').remove();
    img_container = window.frames[0].document.getElementById(img + 'container');
    image = window.frames[0].document.getElementById(img);
    img_container.insertAdjacentElement("beforebegin", image);
    img_container.remove();
}

function first_stage_edit_img(img){
    image = window.frames[0].document.getElementById(img);
    document.getElementById('representative-img').src= image.src;
    img_title.value = image.title;
    document.querySelector('input[name="image_align"][value ="'+ image.align+ '"]').checked = true;
    $('#modal2').modal('open');
    add_img.className = 'waves-effect waves-light btn green hide';
    edit_img.value = img;
    edit_img.className = 'waves-effect waves-light btn green';
}

function second_stage_edit_img(img){
    image = window.frames[0].document.getElementById(img);
    image.align = document.querySelector('input[name="image_align"]:checked').value;
    image.title = img_title.value;
    image.dataset.caption = img_title.value;
    if (img_size_selector[img_size_selector.selectedIndex].value != 'custom') {
         image.style.width = img_size_selector[img_size_selector.selectedIndex].value + '%';
         image.style.height = 'auto';
    }
    else{
        image.style.width = width_input.value;
        image.style.height = height_input.value;
    }
    $('#modal2').modal('close');
    console.log('image edited')
    reset_add_image_menu();
}

function create_img_tools(img){
    image = window.frames[0].document.getElementById(img);
    if (image.parentNode == post_text) {
        var img_container = document.createElement('div');
        img_container.id = img + 'container';
        img_container.style = "white-space: nowrap";
        img_container.onmouseleave=function(){
            remove_img_tools(img);
        }
        img_tools_container = document.createElement('div');
        img_tools_container.id = img + 'tools_container';
        img_tools_container.style = "position: absolute;z-index:10;white-space: normal;display: inline-block;margin-top:10px; margin-left:" + String(image.offsetLeft + 10) + "px;";
        img_tools_container.className = "img_tools_container";
        var remove_img_icon = document.createElement('i');
        remove_img_icon.className = "material-icons";
        remove_img_icon.innerHTML = 'delete';
        var remove_img_tool = document.createElement('a');
        remove_img_tool.className = "btn center";
        remove_img_tool.id = img + 'remove';
        remove_img_tool.onclick = function(){
            img_container.remove();
        }
        var edit_img_icon = document.createElement('i');
        edit_img_icon.className = "material-icons";
        edit_img_icon.innerHTML = 'edit';
        var edit_img_tool = document.createElement('a');
        edit_img_tool.className="btn";
        edit_img_tool.id = img + 'edit';
        edit_img_tool.onclick= function(){
            first_stage_edit_img(img);
        }
        edit_img_tool.appendChild(edit_img_icon);
        remove_img_tool.appendChild(remove_img_icon);
        image.insertAdjacentElement("beforebegin", img_container);
        img_container.appendChild(img_tools_container);
        img_tools_container.appendChild(remove_img_tool);
        img_tools_container.appendChild(edit_img_tool);
        img_container.appendChild(image);
    }
}
function add_video(){
    var video = prompt("Inserează link-ul la video");
    format('insertHTML', '<div class="video-container"><iframe src="https://www.youtube.com/embed/' + video.slice(-11) + '" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');
    console.log('added video')
}

function format(a,b){
    window.frames[0].document.execCommand(a, false,b);
    window.frames[0].focus();
}