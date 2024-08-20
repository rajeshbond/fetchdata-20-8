from datetime import datetime
import pytz

# Define the IST timezone
def check_day():
  ist = pytz.timezone('Asia/Kolkata')

  # Get current date and time in UTC and convert to IST
  now_utc = datetime.now(pytz.utc)
  now_ist = now_utc.astimezone(ist)

  # Get the current day of the week (0=Monday, 6=Sunday)
  day_of_week = now_ist.weekday()

  # Define a list of day names
  days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

  # Print the current day of the week
  # print(f"Today is {days_of_week[day_of_week]} in IST.")

  # Check if today is Saturday or Sunday
  # if day_of_week == 5 or day_of_week == 6:
  #     print("Today is a weekend (Saturday or Sunday) in IST.")
  # else:
  #     print("Today is a weekday in IST.")

  return days_of_week[day_of_week]

check_day()