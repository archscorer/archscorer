### User authentication

* User authentication is solved by django allauth module. Login/singup and few other
  views have copied and overwritten to accommodate archscorer styling.
  _Note: allauth views use independent styling and bootstrap instead of vue and vuetify.
  Keep that in mind for future updates! Styles are mostly collected to base.html_
  By default there is also 'vue' component (AppLoginDialog) that should primarily handle
  user login by email or by third party.

### Shootoffs and Finals
* shootoff is markerd under the type of a course. If creating new shootoff course,
  make sure to assign it correct type.
  Courses with type 's' are not used to compute sum, but its score is used for
  ordering if it is real value (not 0, null, undefined).
  In addition, it is not checked, but 'shootoff' course should appear only once
  per event.
