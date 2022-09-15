const ul = document.querySelector(".tag-ul"),
input = document.querySelector(".tag-input"),
tagNumb = document.querySelector(".tag-details span");
let maxTags = 10,
tags = [];
countTags();
createTag();
function countTags(){
    tagNumb.innerText = maxTags - tags.length;
}
function createTag(){
    ul.querySelectorAll("li").forEach(li => li.remove());
    tags.slice().reverse().forEach(tag =>{
        let liTag = `<li data-value="tag">${tag} <input name="tag" hidden value="${tag}">
					 <i class="uit uit-multiply" onclick="remove(this, '${tag}')"></i></li>`;
        ul.insertAdjacentHTML("afterbegin", liTag);
    });
    countTags();
}
function remove(element, tag){
    let index  = tags.indexOf(tag);
    tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
    element.parentElement.remove();
    countTags();
}
function addTag(e){
    if(e.key === " "){
        let tag = e.target.value.replace(/\s+/g, ' ');
        if(tag.length > 1 && !tags.includes(tag)){
            if(tags.length < 10){
                tag.split(',').forEach(tag => {
                    tags.push(tag);
                    createTag();
                });
            }
        }
        e.target.value = "";
    }
}
input.addEventListener("keyup", addTag);
const removeBtn = document.querySelector(".tag-details .remove-tag");
removeBtn.addEventListener("click", () =>{
    tags.length = 0;
    ul.querySelectorAll("li").forEach(li => li.remove());
    countTags();
});

let survey_options = document.getElementById('survey_options');
let add_more_fields = document.getElementById('add_more_fields');
let remove_fields = document.getElementById('remove_fields');


add_more_fields.onclick = function(){
	let newField = document.createElement('input');
	newField.required = true;
	newField.setAttribute('type','text');
	newField.setAttribute('name','choice');
	newField.setAttribute('class','survey_options');
	newField.setAttribute('size','100');
	newField.setAttribute('placeholder','Choice field');
	newField.setAttribute('minlength', '5')
	newField.setAttribute('maxlength', '200')
	let elseField = document.createElement('input');
	elseField.required = true;
	elseField.setAttribute('type','text');
	elseField.setAttribute('name','choice');
	elseField.setAttribute('class','survey_options');
	elseField.setAttribute('size','100');
	elseField.setAttribute('placeholder','Choice field');
	elseField.setAttribute('minlength', '5')
	elseField.setAttribute('maxlength', '200')
	let newDivField = document.createElement('p')
	let otherDivField = document.createElement('p')
	let newSmallField = document.createElement('small')
	let elseSmallField = document.createElement('small')
	newDivField.append(newField, newSmallField)
	otherDivField.append(elseField, elseSmallField)
	let input_tags = survey_options.getElementsByTagName('input');
	if(input_tags.length === 0) {
		survey_options.append(newDivField, otherDivField);
	}
	else if(input_tags.length < 10) {
		survey_options.append(newDivField);
	}
}

remove_fields.onclick = function(){
	let input_tags = survey_options.getElementsByTagName('p');
	if(input_tags.length === 2) {
		survey_options.removeChild(input_tags[(input_tags.length) - 1]);
		survey_options.removeChild(input_tags[(input_tags.length) - 1]);
	}
	else if(input_tags.length > 2) {
		survey_options.removeChild(input_tags[(input_tags.length) - 1]);
	}
}
