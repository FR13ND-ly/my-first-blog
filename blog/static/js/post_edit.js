var code_part_of_post = document.getElementById('code_part_of_post');
var text_of_post_input = document.getElementById('visual_part_of_post');
var numberofquestions = document.querySelectorAll(".variantinput");
document.getElementById("numberofquestions").value = numberofquestions.length;

function set_post_code_like_text(){
    code_part_of_post.value =document.createTextNode(text_of_post_input.innerHTML).wholeText;
    inarticle_img_list = text_of_post_input.querySelectorAll('img');
    for (i = 0; i < inarticle_img_list.length; i++){
        inarticle_img_list[i].addEventListener("click", function(e){create_img_tools(e.target.id);}, true);
    } 
}

set_post_code_like_text();

function set_text_or_code(type){
    set_text_or_code_btn = document.getElementById("set_text_or_code_btn");
    if (Boolean(Number(type))){
        text_of_post_input.style.display = 'none';
        code_part_of_post.style.display = 'block';
        set_text_or_code_btn.innerHTML = "Text";
        set_text_or_code_btn.value = 0;
    }
    else {
        text_of_post_input.style.display = 'block';
        code_part_of_post.style.display = 'none';
        set_text_or_code_btn.innerHTML = "Cod";
        set_text_or_code_btn.value = 1;
    }
}

function putrandomsurvey(){
    randomsurvey = [['Cat de tare va placut acest articol?', ['1','2','3','4','5'], 'radio'],['Cat de tare va placut acest articol?', ['1','2','3','4','5'], 'checkbox'],['V-a placut acest articol?', ['Da','Nu'], 'radio'],['Ce puteti spune despre acest articol?', ['nesatisfacator','Satisfacator','Bun','Foarte bun'], 'checkbox'],['Ce puteti spune despre acest articol?', ['nesatisfacator','Satisfacator','Bun','Foarte bun'], 'radio']];            
    var oldquestions = document.querySelectorAll(".variantinput");
    var surveyinputs = document.getElementById('surveyvariants');
    var oldbrs = document.querySelectorAll(".variantbr");
    var oldchecks = document.querySelectorAll(".variantcheck");
    var oldmbtns = document.querySelectorAll(".variantmbtn");
    var question = document.getElementById('survey_question');
    a  = Math.floor(Math.random() * (randomsurvey.length));
    document.getElementById("numberofquestions").value = randomsurvey[a][1].length;
    question.innerHTML = randomsurvey[a][0];
    if (randomsurvey[a][2] == 'checkbox'){
        document.getElementById('checkinsurvey').checked = true;
    }
    for (i = 1; i < randomsurvey[a][1].length +1; i++){
        var surveyvariants = document.getElementById('surveyvariants');
        var inputinsurvey = document.createElement("input");
        inputinsurvey.id = 'input' + String(i);
        inputinsurvey.name = 'd';
        inputinsurvey.type = randomsurvey[a][2];
        inputinsurvey.className = 'variantcheck';
        var textinput = document.createElement("input");
        textinput.id = 'textinput' + String(i);
        textinput.placeholder = String(i);
        textinput.required = true;
        textinput.value = randomsurvey[a][1][i-1];
        textinput.name = 'textofvariant' + String(i);
        textinput.className = 'variantinput';
        var minusquestion = document.createElement("button");
        minusquestion.id = 'minusquestion' + String(i);
        minusquestion.value = String(i);
        minusquestion.className = 'variantmbtn';
        minusquestion.innerHTML = '-';
        var br = document.createElement("br");
        br.id = 'br' + String(i);
        br.className = 'variantbr';
        minusquestion.onclick = function() {
            surveyvariants.removeChild(document.getElementById('input' + minusquestion.value));
            surveyvariants.removeChild(document.getElementById('textinput' + minusquestion.value)   );
            surveyvariants.removeChild(document.getElementById('minusquestion' + minusquestion. value));
            surveyvariants.removeChild(document.getElementById('br' + minusquestion.value));
        }
        surveyvariants.appendChild(inputinsurvey);
        surveyvariants.appendChild(textinput);
        surveyvariants.appendChild(minusquestion);
        surveyvariants.appendChild(br);
    }
            

        for (i = 0; i < Number(oldquestions.length) ; i++){
            surveyinputs.removeChild(oldquestions[i]);
            surveyinputs.removeChild(oldbrs[i]);
            surveyinputs.removeChild(oldchecks[i]);
            surveyinputs.removeChild(oldmbtns[i]);
        } 
}

function deletequestion(number){
    var surveyinputs = document.getElementById('surveyvariants');
    surveyinputs.removeChild(document.getElementById('input' + number));
    surveyinputs.removeChild(document.getElementById('textinput' + number));
    surveyinputs.removeChild(document.getElementById('minusquestion' + number));
    surveyinputs.removeChild(document.getElementById('br' + number));
}

function addquestion(){
    currentvariant = Number(document.getElementById('numberofquestions').value) + 1;
    var surveyvariants = document.getElementById('surveyvariants');
    var inputinsurvey = document.createElement("input");
    inputinsurvey.id = 'input' + String(currentvariant);
    inputinsurvey.name = 'd';
    inputinsurvey.className = 'variantcheck';
    var textinput = document.createElement("input");
    textinput.id = 'textinput' + String(currentvariant);
    textinput.placeholder = String(currentvariant);
    textinput.required = true;
    textinput.name = 'textofvariant' + String(currentvariant);
    textinput.className = 'variantinput';
    var minusquestion = document.createElement("button");
    minusquestion.id = 'minusquestion' + String(currentvariant);
    minusquestion.value = String(currentvariant);
    minusquestion.className = 'variantmbtn';
    var br = document.createElement("br");
    br.id = 'br' + String(currentvariant);
    br.className = 'variantbr';
    minusquestion.innerHTML = '-';
    minusquestion.onclick = function() {
        surveyvariants.removeChild(document.getElementById('input' + minusquestion.value));
        surveyvariants.removeChild(document.getElementById('textinput' + minusquestion.value));
        surveyvariants.removeChild(document.getElementById('minusquestion' + minusquestion.value));
        surveyvariants.removeChild(document.getElementById('br' + minusquestion.value));
    //    document.getElementById('numberofquestions').value = Number(document.getElementById('numberofquestions').value) - 1;
    }

    inputinsurvey.type = 'radio';
    surveyvariants.appendChild(inputinsurvey);
    surveyvariants.appendChild(textinput);
    surveyvariants.appendChild(minusquestion);
    surveyvariants.appendChild(br);
    document.getElementById('numberofquestions').value = currentvariant;
}

function typeofcheckinsurvey(type){
    for (i = 1; i < Number(document.getElementById('numberofquestions').value) + 1; i++) {
        inputinsurvey = document.getElementById('input' + String(i));
        inputinsurvey.type = type;
        }
}

function set_post_text_like_code(){ 
    text_of_post_input.innerHTML = code_part_of_post.value;
}

function f(a, b) {
    document.execCommand(a, false, b);
    text_of_post_input.focus();
    set_post_text_like_code();
}
        
function set_representative_cover_of_post(){
    var post_cover_input = document.getElementById("file-input");
    var representative_cover = document.getElementById("post_cover");
    representative_cover.src = URL.createObjectURL(post_cover_input.files[0]);
}

function edit_img_menu(edit_image=false){  
    var edit_img_window = document.getElementById("edit_image_menu");
    edit_img_window.style.display = 'block';
    var close_menu_btn = document.getElementById("close_editmenu_btn");
    var save_img = document.getElementById("save_img_btn");
    var img_input = document.getElementById("file-in-article-input")
    var img_size_selector = document.getElementById('img_size_selector');
    var img_title_input = document.getElementById('img_title');
    var custom_width_input = document.getElementById('custom_width_input');
    var custom_height_input = document.getElementById('custom_height_input');
    var custom_img_sizes = false;
    var img_style ="border:1px solid #ccc;position:relative;object-fit: cover;overflow: hidden; border-radius: 5px"; 
    
    //default image width and height
    var img_width = 300;
    var img_height = 200;

    var representative_img = document.getElementById("representative_img");

    if (edit_image){
        save_img.type = 'button';
        var representative_img_src = 'http://127.0.0.1:8000/media//blog/static/media/' + edit_image;
        document.querySelector(('input[tag="image_align"][value = "'+ document.getElementById(edit_image).align +'"]')).checked = true;
        img_title_input.value = document.getElementById(edit_image).title;
    }
    else{
        save_img.type = 'submit';
        var representative_img_src = URL.createObjectURL(img_input.files[0]);  
    }

    representative_img.src = representative_img_src;

    close_menu_btn.onclick = function(){
        edit_img_window.style.display = "none";
    }

    img_size_selector.onchange = function(){
        if(img_size_selector[img_size_selector.selectedIndex].value == 'small'){
            img_width = 150;
            img_height = 150;
        }
         if(img_size_selector[img_size_selector.selectedIndex].value == 'normal'){
            img_width = 300;
            img_height= 200;
        }
        if(img_size_selector[img_size_selector.selectedIndex].value == 'big'){
            img_width = 900;
            img_height = 600;
        }
        if(img_size_selector[img_size_selector.selectedIndex].value == 'custom'){
            custom_width_input.style.display = "block";
            custom_height_input.style.display = "block";
            custom_img_sizes = true;
        }
        img_size_selector.selectedIndex=0; 
    }
    save_img.onclick = function(){
        var img_title_input = document.getElementById('img_title');
        var img_align = document.querySelector('input[tag="image_align"]:checked').value;
        var img_title = img_title_input.value;
        if (custom_img_sizes){
            img_width = custom_width_input.value;
            img_height = custom_height_input.value;
            custom_width_input.style.display = 'none';
            custom_height_input.style.display = 'none';
        }
        if (!edit_image){
            var image = "<img src='" + 'http://127.0.0.1:8000/media//blog/static/media/' + img_input.files[0].name + "' width= '" + String(img_width)+ "' id='"+ img_input.files[0].name + "' height='" + String(img_height) + "' title = '" + img_title + "' align = '" + img_align + "' style='" + img_style + "' onclick="+ '"' +"create_img_tools('" + img_input.files[0].name + "')" + '"' + ">";
            text_of_post_input.focus();
            f("insertHTML" , image);
        }
        else{                   
            image = document.getElementById(edit_image);
            image.height = img_height;
            image.width = img_width;
            image.align = img_align;
            image.title = img_title;
            set_post_code_like_text();
        }
        img_title_input.value = '';
        edit_img_window.style.display = "none";
        document.querySelector('input[tag="image_align"][value="left"]').checked =true;
    }
}

function create_img_tools(img){
    if (!document.getElementById(img + 'remove')){
        var img_container = document.createElement('text_of_post_input');
        img_container.id = img + 'container';
        img_container.onmouseleave = function(){
            remove_img_tools(img);
        }
        var remove_img_tool = document.createElement('button');
        remove_img_tool.id = img + 'remove';
        remove_img_tool.innerHTML = 'x';
        remove_img_tool.type = 'button';
        remove_img_tool.onclick = function(){
            img_container.remove()
            set_post_code_like_text()
        }
        var edit_img_tool = document.createElement('button');
        edit_img_tool.id = img + 'edit';
        edit_img_tool.innerHTML = 'edit';   
        edit_img_tool.type = 'button';
        edit_img_tool.onclick = function(){
            edit_img_menu(img);
        }
        image = document.getElementById(img);
        image.insertAdjacentElement("beforebegin", img_container);
        img_container.appendChild(image);
        img_container.appendChild(remove_img_tool);
        img_container.appendChild(edit_img_tool);
        set_post_code_like_text();
    }
}

function remove_img_tools(img){
    document.getElementById(img + 'remove').remove();
    document.getElementById(img + 'edit').remove();
    img_container = document.getElementById(img + 'container');
    image = document.getElementById(img);
    img_container.insertAdjacentElement("beforebegin", image);
    img_container.remove();
    set_post_code_like_text();
}