# The noreply spoofing doesn't work unless we have our own email server. 
# Gmail overwrites it

EMAIL_SENDER = 'Perfit Backend Team <noreply@perfit.info>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'perfitbackendteam'
EMAIL_HOST_PASSWORD = 'jr37hNVKCQSfBgGa'
EMAIL_USE_SSL = True