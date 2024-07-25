from datetime import datetime, timezone, timedelta

pst = timezone(timedelta(hours=-8))

def countdown(day_param):
  today = datetime.today().astimezone(pst)

  diff = day_param - today
  days = diff.days
  hours, rem = divmod(diff.seconds, 3600)
  minutes, seconds = divmod(rem, 60)

  return days, hours, minutes, seconds