from datetime import datetime, timezone, timedelta

pst = timezone(timedelta(hours=-8))
japan_date = datetime(2025, 1, 1, tzinfo=pst)

def countdown():
  today = datetime.today().astimezone(pst)

  diff = japan_date - today
  days = diff.days
  hours, rem = divmod(diff.seconds, 3600)
  minutes, seconds = divmod(rem, 60)

  return days, hours, minutes, seconds