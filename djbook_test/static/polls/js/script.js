let choices = document.getElementById('choices_id');
let add_choice_fields = document.getElementById('add_choice_fields');
let remove_choice_fields = document.getElementById('remove_choice_fields');


add_choice_fields.onclick = function(){
	let newField = document.createElement('input');
	newField.required = true;
	newField.setAttribute('type','text');
	newField.setAttribute('name','choice');
	newField.setAttribute('class','choices');
	newField.setAttribute('size','100');
	newField.setAttribute('placeholder','Choice field');
	newField.setAttribute('minlength', '5');
	newField.setAttribute('maxlength', '200');
	let otherField = document.createElement('input');
	otherField.required = true;
	otherField.setAttribute('type','text');
	otherField.setAttribute('name','choice');
	otherField.setAttribute('class','choices');
	otherField.setAttribute('size','100');
	otherField.setAttribute('placeholder','Choice field');
	otherField.setAttribute('minlength', '5');
	otherField.setAttribute('maxlength', '200');
	let input_tags = choices.getElementsByTagName('input');
	if(input_tags.length === 0) {
		choices.append(newField);
		choices.append(otherField)
	}
	else if(input_tags.length < 10) {
		choices.append(newField);
	}
};

remove_choice_fields.onclick = function(){
	let input_tags = choices.getElementsByTagName('input');
	if(input_tags.length === 2) {
		choices.removeChild(input_tags[(input_tags.length) - 1]);
		choices.removeChild(input_tags[(input_tags.length) - 1]);
	}
	else if(input_tags.length > 2) {
		choices.removeChild(input_tags[(input_tags.length) - 1]);
	}
}

let tags = document.getElementById('tags_id');
let add_tag_fields = document.getElementById('add_tag_fields');
let remove_tag_fields = document.getElementById('remove_tag_fields');


add_tag_fields.onclick = function(){
	let newField = document.createElement('input');
	newField.required = true;
	newField.setAttribute('type','text');
	newField.setAttribute('name','tag');
	newField.setAttribute('class','tags');
	newField.setAttribute('size','100');
	newField.setAttribute('placeholder','Tag field');
	newField.setAttribute('minlength', '5');
	newField.setAttribute('maxlength', '200');
	let input_tags = tags.getElementsByTagName('input');
	if(input_tags.length < 10) {
		tags.append(newField);
	}
};

remove_tag_fields.onclick = function(){
	let input_tags = tags.getElementsByTagName('input');
	tags.removeChild(input_tags[(input_tags.length) - 1]);
}

