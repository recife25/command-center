from outlook_module import OutlookCalendar

oc = OutlookCalendar()
events = oc.list_events()
print(events)
