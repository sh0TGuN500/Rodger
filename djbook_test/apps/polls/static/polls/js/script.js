let survey_options = document.getElementById('survey_options');
let add_more_fields = document.getElementById('add_more_fields');
let remove_fields = document.getElementById('remove_fields');

add_more_fields.onclick = function(){
	let newField = document.createElement('input');
	newField.required = true;
	newField.setAttribute('type','text');
	newField.setAttribute('name','choice');
	newField.setAttribute('class','survey_options');
	newField.setAttribute('size',100);
	newField.setAttribute('placeholder','Choice field');
	let elseField = document.createElement('input');
	elseField.required = true;
	elseField.setAttribute('type','text');
	elseField.setAttribute('name','choice');
	elseField.setAttribute('class','survey_options');
	elseField.setAttribute('size',100);
	elseField.setAttribute('placeholder','Choice field');
	let input_tags = survey_options.getElementsByTagName('input');
	if(input_tags.length === 0) {
		survey_options.append(newField, elseField);
	}
	else if(input_tags.length < 10) {
		survey_options.append(newField);
	}
}

remove_fields.onclick = function(){
	let input_tags = survey_options.getElementsByTagName('input');
	if(input_tags.length === 2) {
		survey_options.removeChild(input_tags[(input_tags.length) - 1]);
		survey_options.removeChild(input_tags[(input_tags.length) - 1]);
	}
	else if(input_tags.length > 2) {
		survey_options.removeChild(input_tags[(input_tags.length) - 1]);
	}
}
