const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});


function validateForm() {
	var response = grecaptcha.getResponse();
  
	if (response.length === 0) {
	  alert("Please complete the reCAPTCHA verification.");
	  return false;
	} else {
	  // reCAPTCHA verification passed, submit the form
	  document.querySelector('form').submit();
	}
  }




  