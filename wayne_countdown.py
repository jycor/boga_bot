from datetime import datetime, timezone, timedelta

pst = timezone(timedelta(hours=-8))
wayne_date = datetime(2024, 8, 14, tzinfo=pst)

def countdown():
  today = datetime.today().astimezone(pst)

  diff = wayne_date - today
  days = diff.days
  hours, rem = divmod(diff.seconds, 3600)
  minutes, seconds = divmod(rem, 60)

  return days, hours, minutes, seconds