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
 * Name (IV klubide karikas)
 * Date (22.10.20)
 * Description (bla, bla, maksab bla, süüa saab bla)
 * Course / place ID -- string (Räbiküla)
 * Format (Animal / Field, etc)
 * Ends
  * ID - numeric
  * Description (optional) - 'Kits' / '35 fan'
  * nr of arrows - numeric
  * allowed scores - numeric list (1..5 / 20,18,16,14,12,10 - 'M/-') negative values are also allowed
 * Participants
  * ID (uniq) - refers to Archers database (site users) [people registered by name only get every time new ID, once they register - all entries with such name are pulled together and tables are updated to new ID]
  * Ends
   * ID
   * arrow scores
  * Cum score (computed)
