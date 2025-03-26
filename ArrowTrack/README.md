# shotTracker
track my weekly arrow count


# Overview

1) Data Stored in postgress database
2) modular approach
3) data only for now, then add nicegui front end

## Notes
1) must use source control
2) secrets in separate file added to .gitignore


## Process
### Main.py - Reserved for front end
### Get_events
Pull all events from connected calendars
### write_events
CRUD function to keep mailbox in sync with db





## Future functionality
1) build a "subscription" service (email notifications of new events trigger a workflow to add events to the calendar)
2) add secrets to aws secrets manager
