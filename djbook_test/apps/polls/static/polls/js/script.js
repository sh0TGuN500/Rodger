// show a message with a type of the input
function showMessage(input, message, type) {
	// get the small element and set the message
	const msg = input.parentNode.querySelector("small");
	msg.innerText = message;
	// update the class for the input
	input.className = type ? "success" : "error";
	return type;
}

function showError(input, message) {
	return showMessage(input, message, false);
}

function showSuccess(input) {
	return showMessage(input, "", true);
}

function hasValue(input, message) {
	if (input.value.trim() === "") {
		return showError(input, message);
	}
	return showSuccess(input);
}

const form = document.querySelector("#add_question");
const choiceForm = form.querySelector("#question_form");

const TITLE_REQUIRED = "Please enter your title";
const TEXT_REQUIRED = "Please enter your question text";
const CHOICE_REQUIRED = "Please enter your choice";

form.addEventListener("submit", function (event) {
	// stop form submission
	event.preventDefault();

	// validate the form
	let titleValid = hasValue(form.elements["question_title"], TITLE_REQUIRED);
	let textValid = hasValue(form.elements["question_text"], TEXT_REQUIRED);
	let elements_length = form.elements.length
	//console.log(form.elements)
	if (elements_length >= 6) {
		let choiceArray = []
		for (let i = 3; i < elements_length - 1; i++) {
			var choiceValid = hasValue(form.elements[i], CHOICE_REQUIRED)
			choiceArray.push(choiceValid)
		}
		let everyChoiceValid = choiceArray.every(Boolean)
		var valid = (titleValid && textValid && everyChoiceValid)
	}
	else {
		var valid = (titleValid && textValid)
	}
	// if valid, submit the form.
	if (valid) {
		document.getElementById("add_question").submit();
	}
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
	let elseField = document.createElement('input');
	elseField.required = true;
	elseField.setAttribute('type','text');
	elseField.setAttribute('name','choice');
	elseField.setAttribute('class','survey_options');
	elseField.setAttribute('size','100');
	elseField.setAttribute('placeholder','Choice field');
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
