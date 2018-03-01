
	var failIcon = '&#10007;'; // x
	var passIcon = '&#10003;'; // checkmark
	var passwordValidated = false;
	var inviteValidated = false;
	var usernameValidated = false;
	
	function successIcon(elemID, icon, status) {
		
		if (status == "success") document.getElementById(elemID).style.color = "green";
	
		else  if (status == "fail") document.getElementById(elemID).style.color = "red";

		document.getElementById(elemID).innerHTML = icon;
	}


	function ajaxValidation(valueType, value, elemID, formObj) {

		if (value != "") {
			var url;
			var csrftoken = Cookies.get('csrftoken');
			postData = valueType + "=" + value;

			if (valueType == "username") url = "username-availability";
			else if (valueType == "invite_code") {
				url = "invite-code-validation";
				postData = getPostData(formObj);
			}

			var xmlhttp = new XMLHttpRequest();
	   		xmlhttp.open("POST", url, true);
	   		xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	   		xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	   		xmlhttp.send(postData);

	   		xmlhttp.onreadystatechange = function() {
			    if (this.readyState == 4 && this.status == 200) {
			        var jsonObj = JSON.parse(this.responseText);
			        if (jsonObj.status == 'SUCCESS') {
			        	successIcon(elemID, passIcon, "success");

			        	if (valueType == "username") usernameValidated = true;
			        	else if (valueType == "invite_code") {
			        		inviteError(false);
			        		inviteValidated = true;
			        	}
			        }
			        else {
			        	successIcon(elemID, failIcon, "fail");
			        	if (valueType == "username") usernameValidated = false;
			        	else if (valueType == "invite_code") inviteValidated = false;
			        }	
			    }
			};
   		}
   		else successIcon(elemID, "", "reset");

	}

	function usernameExists(input) {

		ajaxValidation("username", input.value, "username-exists", null);
	}
	function inviteError(error) {
		inviteValidated = false;

		if (!error) {
			document.getElementById("presubmission-message").innerHTML = "";
			inviteValidated = true;
		}		
		else {
			var html = "Sorry, the invitation code you've provided is invalid.";
			html 	+= " Possible reasons for failure:";
			html 	+= "<ul>";
			html 	+= "<li>The invitation code may have been redeemed already</li>";
			html 	+= "<li>The invitation code belongs to someone else</li>";
			html 	+= "</ul>";
			html 	+= "Make sure you have entered the invitation code, first name,";
			html 	+= " last name, and email address exactly as shown in the";
			html 	+= " invitation email. If the problem continues, please contact support.";
			document.getElementById("presubmission-message").innerHTML = html;
		}

	}

	function validateInvite(input, formObj) {

		inviteValidated = false;
		if (input.value == "") {
			document.getElementById("presubmission-message").innerHTML = "";
			successIcon('invite-is-valid', "", "reset");
		}
		else if (input.value.length > 0 && input.value.length != 36) {
			successIcon("invite-is-valid", failIcon, "fail");
			inviteError(true);
		}
		else if (input.value.length == 36 ) {
			ajaxValidation("invite_code", input.value, "invite-is-valid", formObj);
	}
}

	function loadForm(formID) {

		if (formID == "signup") {
			document.getElementById("password-reset").style.display = "none";
			document.getElementById("signup").style.display = "block";
			document.getElementById("login").style.display = "none";
		}
		else if (formID == "login") {
			document.getElementById("password-reset").style.display = "none";
			document.getElementById("signup").style.display = "none";
			document.getElementById("login").style.display = "block";
		}
		else if (formID = "password-reset") {
			document.getElementById("password-reset").style.display = "block";
			document.getElementById("signup").style.display = "none";
			document.getElementById("login").style.display = "none";

		}

	}

	function patternMatch(string) {

		var pattern = /^(\w+){8,}$/; //at least eight characters and alphanumeric
		matchArr =  string.match(pattern);
		if (matchArr != null && matchArr.length > 0) return true;
		return false;
	}

	function passwordMatch() {
	
		var password1 = document.getElementById('password1').value;
		var password2 = document.getElementById('password2').value;
		passwordValidated = false;

		if (password1 != "" && password1 == password2 && patternMatch(password1)) {
			successIcon('password-match', passIcon, "success"); 
			passwordValidated = true;
		}
		else if ((password2 != "" && password1 != password2) || 
			(password2 != "" && !patternMatch(password1))) {
				successIcon('password-match', failIcon, "fail");
			}
		else {
			successIcon('password-match', "", "reset");
		}
	}
	
	function getPostData(formObj) {


		var fName 	= formObj.first_name.value;
		var lName 	= formObj.last_name.value;
		var uName 	= formObj.username.value;
		var email 	= formObj.email.value;
		var password = formObj.password1.value;
		var team =	formObj.team.value;
		var invite = formObj.invite_code.value;

		var querystring = 'first_name=' + fName + '&last_name=' + lName + '&username=';
		querystring += uName + '&email=' + email + '&password1=' + password;
		querystring += '&team=' + team + '&invite_code=' + invite;

		return querystring;

	}
	
	
	function formSubmit(formObj) {

		// Submit form synchronously and wait for submission status
		
		if (passwordValidated && inviteValidated && usernameValidated) {
	
			var querystring = getPostData(formObj);
			var csrftoken = Cookies.get('csrftoken');
			var xmlhttp = new XMLHttpRequest();
	   		xmlhttp.open("POST", "registration", false);
	   		xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	   		xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	   		xmlhttp.send(querystring);

	   		jsonObj = JSON.parse(xmlhttp.responseText);
	   		if (jsonObj.status == 'SUCCESS') thankyouPage();
	   		else registrationFail();
	   	}
	   	else {
	   		registrationFail();
	   	}

	}

	function thankyouPage() {

		var html = "<div class=\"message\" id=\"registration-thankyou\">";
		html += "Thank you for registering. Please click <a href=\"\\\">Here</a>";
		html += " to be redirected.</div>"
		document.getElementById("registration-form").innerHTML = html;
	}

	function registrationFail() {

		var html = "Unable to create an account. Please";
		html += " verify your information and try again. If the problem continues, contact support.";
		html += " <a id=\"registration-fail\" onclick=\"reloadRegistration()\">Take me Back</a>"
		
		document.getElementById("registration-form").innerHTML = html;
		document.getElementById("registration-form").style.color = "#636363";
	}

	function reloadRegistration() {
		window.location.href = "/";
	}

	function userLogin(formObj) {

		var username = formObj.username.value;
		var password = formObj.password.value;
		var qs = "username="+username+"&password="+password;

		var csrftoken = Cookies.get('csrftoken');
		var xmlhttp = new XMLHttpRequest();
   		xmlhttp.open("POST", "login", false);
   		xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
   		xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
   		xmlhttp.send(qs);

   		if (xmlhttp.responseURL.includes("login")){
   			document.getElementById("login-message").innerHTML = "Username or password not recognized"
   		}
   		else {
   			// Redirect to the landingp page
   			window.location.href = xmlhttp.responseURL;
   		}
	}

	function passwordReset(formObj) {

		var email = formObj.email.value;
		var qs = "email="+email;

		var csrftoken = Cookies.get('csrftoken');
		var xmlhttp = new XMLHttpRequest();
   		xmlhttp.open("POST", "password-reset", false);
   		xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
   		xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
   		xmlhttp.send(qs);

   		var html = "<div class=\"message\" id=\"password-reset-message\">Please check your email for a password reset link. ";
		html += " <a href=\"/\">Take me Back</a></div>";

		document.getElementById("password-reset").innerHTML = html;

	}