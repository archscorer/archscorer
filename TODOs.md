# TODOs


* https://github.com/rsinger86/drf-access-policy/ -- good idea before going public
* https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions -- is another way to go


* add some kind of contact admin page?

Iga vibu harjutuse per class top tulemused aasta lõikes

archiving event should set some backend limitations as well.. some more tests and
limitations on frontend on combined with registration switch.

ja kui statistikat teha, siis ntg per võistlus: osalejaid kokku A/V osalejaid /C/J osalejad, lastud rekordid

Scorecard editing capability. Event creator or admin should be able to create scorecards without arrows
 (i.e. only scores and spots are marked on scorecard).
 As well there should be 'checked' flag on ScoreCard that event admin can click while checking scores
 on paper vs virtual. This click would also trigger class_level and record check!

Make archer-club relation many to many. Same archer can have several clubs. It will
be a bit more confusing when registration happens. When registering to an event archer
needs to select club that they represent on given competition. Club will then remain
tied to participant object.
  Many to many and changeable relation between archer and clubs will allow to eliminate
all double archer profiles.

For participants, groups, ends and positions might need per round approach. So pools
or groupings would be reserved for previous round as well. This would also lay ground-
work for one possible duel system generation.
  Might need to think of another totally separate duel system (in separate tab on the
event page?).

Records update EE -> FAAE

UPDATE api_record SET scope = REPLACE(scope, 'EE', 'FAAE') WHERE scope LIKE '%EE%';

* write update database to fill new particiant gender, full_name and archer_rep
* club associations need to be redone, due to schema change

before release:
* participant full_name from participant model, not archer. fill in in participant registration
 -> update api_participant p inner join api_archer a on p.archer_id = a.id set p.full_name = a.full_name;
* participant gender from participant model, not archer. fill in in participant registration
 -> update api_participant p inner join api_archer a on p.archer_id = a.id set p.gender = a.gender;
* participant club short --> particiant archer_rep. fill in in participant registration -- this
  is more clomplicated as might need selections by user.
  Probably one dropdown to choose club
* add association also to the event - this will allow to filter competitions per association.

* Add rule system for competitions, basically either WA or IFAA. It will change how bow
styles and classes are displayed in results page, that shuold be all in the first iteration
