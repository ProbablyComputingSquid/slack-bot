from main import convertDate,parse_time
import pytz

print(convertDate("6:30am PST CST".split()))
print(parse_time("June 6, 2025"))
print(parse_time("6:30am June 6, 2025"))
#print(pytz.timezone("PST"))
#print(pytz.common_timezones)
print(parse_time("17:07 June 9, 2025"))
