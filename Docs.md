### User authentication

User authentication is solved by django allauth module. Login/singup and few other
views have copied and overwritten to accommodate archscorer styling.
_Note: allauth views use independent styling and bootstrap instead of vue and vuetify.
Keep that in mind for future updates! Styles are mostly collected to base.html_
By default there is also 'vue' component (AppLoginDialog) that should primarily handle
user login by email or by third party.
