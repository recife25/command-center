from datetime import datetime, timedelta
from outlook_module import OutlookCalendar

oc = OutlookCalendar()

title = "Command Center Test Event"
start = datetime.now() + timedelta(minutes=5)
end = start + timedelta(hours=1)
description = "Created via API test."

result = oc.create_event(title, start, end, description)
print(result)
