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

function hasValue(input, message, value_len) {
	let value = input.value.trim().replace(/\s+/g, ' ');
	console.log(message)
	if(value.length < value_len){
		return showError(input, message);
	}
	return showSuccess(input);
}

const form = document.querySelector("#add_question");

const TITLE_REQUIRED = "Please enter your title";
const TEXT_REQUIRED = "Please enter your question text";
const CHOICE_REQUIRED = "Please enter your choice";

form.addEventListener("submit", function (event) {
	// stop form submission
	event.preventDefault();

	// validate the form
	let titleValid = hasValue(form.elements["question_title"], TITLE_REQUIRED, 5);
	let textValid = hasValue(form.elements['question_text'], TEXT_REQUIRED, 20)
	let elements_length = form.elements.length
	console.log(elements_length)
	if (elements_length > 6 + tags.length) {
		let choiceArray = []
		for (let i = 5 + tags.length; i < elements_length - 1; i++) {
			var choiceValid = hasValue(form.elements[i], CHOICE_REQUIRED, 5)
			choiceArray.push(choiceValid)
		}
		let everyChoiceValid = choiceArray.every(Boolean)
		console.log(everyChoiceValid)
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