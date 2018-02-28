html = """
<body>
	<span>Hi {},</span>
	<p>
		Welcome to Perfit! <br><br>
		This email contains information you would need to 
		register to use the api documentation site, found at <a href="http://api.perfit.info">api.perfit.info.</a> 
		Please enter the credentials in bold exactly as they are shown. Otherwise,
		you will not be able to register. If you have any questions or are 
		unable to register, please message the backend team on Slack.
	</p>
	<div class="credentials" style="margin-left: 50px">
		First Name: <strong>{}</strong> <br>
		Last Name:	<strong>{}</strong> <br>
		Email:		<strong>{}</strong> <br>
		Invitation Code: <strong>{}</strong> <br>
	</div>
	<p>
		Please visit <a href="http://api.perfit.info">api.perfit.info.</a>  and click on 'Create an account' to register. 
	</p>
	<div class="signature">
		The Backend Team
	</div>
</body>
"""

txt = """
	Hi {},

	Welcome to Perfit! 

	This email contains information you would need to 
	register to use the api documentation site, found at www.api.perfit.info. 
	Please enter the credentials in bold exactly as they are shown. Otherwise,
	you will not be able to register. If you have any questions or are 
	unable to register, please message the backend team on Slack.

		
	First Name: {}
	Last Name:	{}
	Email:		{}
	Invitation Code: {}
		
	Please visit www.api.perfit.info. and click on 'Create an account' to register. 
		

	The Backend Team
"""

def get_template(template_type):

	if template_type == "txt":
		return txt
	return html

