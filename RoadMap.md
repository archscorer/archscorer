# Arch[scor]er

### page layout and hierarchy -- thoughts

Initial simple functionality should include

* Create competition
 * From template (Field, Hunter, Animal, etc)
 * Custom: [number of targets, arrows per target, how to score]

Site Needs to managed past and present competitions, site needs browse / search / blog function to
find competitions. Past competition scores could be private (only participants can see) or public.

* Add participants
 * by registration form (pre-filled for logged in user / can register others as well? / registration by link / payment by bank link?)
* Arrange participants to targets (need some privileges)
 * By class / comp cum score / rating / manual
* Scoring
 * Show running score for the competition
 * Input end score - one arrow at a time, for each competitor at given end

All this requires some user management (Google/FB/email auth)


## Database model for a competition

* New competition
 * ID - uniq / numeric
 * Name (IV klubide karikas)
 * Date (22.10.20) / Date range (multi day competitions)
 * Description (bla, bla, maksab bla, süüa saab bla)
 * Course / place ID -- string (Räbiküla)
 * Format (Animal / Field, etc)
 * tags (i.e. public(official/open) / club / series / private -- used in visibility settings in comp listing, private only visible if logged in and you are registered to that event. public, club, series can be used in filtering and searching. )
 * Ends
  * ID - uniq numeric
  * Description (optional) - 'Kits' / '35 fan'
  * nr of arrows - numeric
  * allowed scores - numeric list (1..5 / 20,18,16,14,12,10 - 'M/-') negative values are also allowed
 * Participants
  * ID (uniq) - refers to Archers database (site users) [people registered by name only get every time new ID, once they register - all entries with such name are pulled together and tables are updated to new ID]
  * class (AMLB, etc)
  * Arrow Scores
   * End ID - refers to competition Ends table?
   * arrow scores
   * end score (computed)
  * Cum score (computed)

## Database model for series (a la Club Cup)

* New series
 * ID - uniq / numeric
 * Name (Klubide Karikas 2019)
 * Stages - list to competitions that belong to series
 * Rules -- not sure how to express that?
  * Allowed clubs (i.e club cup points are only awarded to Estonian clubs, others can participate, but no points will be awarded)
  * max points
 * Participants
  * ID (uniq) - refers to Archers database
  * cum points (computed - from stages, by class)

## Database model for Archer

* New Archer
 * ID - uniq / numeric
 * Name
 * email - email is mandatory for site users (? different database?)
 * club(s)
 * site related fields: roles, password ?
 * birthday (optional) - could be used to filter for eligible classes
 * last - _last.class_, _last.club_ - for registration autofill
