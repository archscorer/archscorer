# TODOs


* https://github.com/rsinger86/drf-access-policy/ -- good idea before going public
* https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions -- is another way to go

* Event list serializer should be separate to event-detail serializer. List serializer
 provides only top level information while details also include results and additional
 information about rounds and participants.
 * event top level serializer has info about rounds, participants only as numberofparticipants

* write my own views for login/logout/signup etc
* write view for user/archer profile
* add some kind of contact admin page?


* add competition overview page (what rounds)
* to competition owner can edit participants / rounds
* competition to have visibility levels
 * training / small competition - personal - only registered users can see
 * club - visible to club members
 * public - visible to all

 * whether it is possible to register is options by owner. Owner can always add
 participants
