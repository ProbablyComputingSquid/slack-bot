import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import re
from datetime import datetime
import pytz
from typing import Optional
    

# Initializes your app with your bot token and socket mode handler
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    # signing_secret=os.environ.get("SLACK_SIGNING_SECRET") # not required for socket mode
)

# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.message("bad boy")
def message_bad_boy(message, say):
    say(f"sowwy~ pwease forgive me 3:") # why did i do this LMAO


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

# convert those temperatures yahhh
# also like who tf uses rankine be fr
def convertTemp(text):
    c = None
    startingUnit = text[0][-1]
    text[0] = text[0][:-1] # this is the actual nunmber
    if startingUnit == "f":
        f = float(text[0])
        c = (f - 32) * 5/9
    elif startingUnit == "c":
        c = float(text[0])
    elif startingUnit == "k":
        k = float(text[0])
        c = k - 273.15
    elif startingUnit == "r":
        r = float(text[0])
        c = (r - 491.67) * 5/9
    
    if c is not None:
        match (text[1]):
            case "f":
                return (f"{text[0]}°{startingUnit.upper()} is {round(c * 9/5 + 32,2)}°F")
            case "k":
                return (f"{text[0]}°{startingUnit.upper()} is {c + 273.15}K")
            case "r":
                return (f"{text[0]}°{startingUnit.upper()} is {round((c + 273.15) * 9/5,2)}R")
            case "c":
                return (f"{text[0]}°{startingUnit.upper()} is {c}°C")
            case _:
                return (f"{text[1]} is an invalid unit")
    else:
        return (f"{startingUnit} is an invalid unit")

# metric table for tconverfting metric units
metricTable = {
    "k" : 1000,      # kilo
    "h" : 100,       # hecto
    "da": 10,        # deka
    "d" : 1/10,      # deci
    "c" : 1/100,     # centi
    "m" : 1/1000,    # milli
    "µ" : 1/1000000, # micro
    "u" : 1/1000000, # alternative for micro
    "n" : 1/1000000000, # nano
}
metricUnits = {
    "g","m","l"
}

# convert lengths 
# how this is gonna work is convert everything -> meters -> convert to the target unit

def convertLength(text:list):
    startingMeasurement = text[0]
    targetUnit = text[1] if len(text) > 1 else "m"  # default to meters if no target specified
    
    pattern = r'^(\d*\.?\d+)([k|h|da|d|c|m|µ|u|n]?)(m|ft|in|yd|mi)$'
    
    match = re.match(pattern, startingMeasurement.lower())
    if not match:
        return "Invalid measurement format. Please use format like: 1.5km, 2m, 3ft, etc."
        
    number = float(match.group(1))
    prefix = match.group(2)
    measurementUnit = match.group(3)
    meters = None
    imperial = False
    # Convert to meters
    if measurementUnit == "m":
        if prefix:
            meters = number * metricTable[prefix]
        else:
            meters = number
    else:  # imperial units
        imperial = True
        feet = number
        match measurementUnit:
            case "yd":
                feet = number * 3
            case "in":
                feet = number / 12
            case "mi":
                feet = number * 5280
            case "ft":
                feet = number
        meters = feet * 0.3048

    # Convert to good ol plain vanilla meters
    if targetUnit == "m":
        return f"{startingMeasurement} is {meters}m"
    
    # Handle metric prefixes
    # Check if target unit is a metric unit with prefix
    if targetUnit.startswith(("k", "h", "da", "d", "c", "m", "µ", "u", "n")) and targetUnit.endswith("m"):
        prefix = targetUnit[0]
        if prefix in metricTable:
            return f"{startingMeasurement} is {meters / metricTable[prefix]}{targetUnit}"
        else:
            return f"Invalid metric prefix: {prefix}"
    
    # Handle imperial units
    feet = meters / 0.3048
    match targetUnit:
        case "ft":
            return f"{startingMeasurement} is {feet}ft"
        case "yd":
            return f"{startingMeasurement} is {feet/3}yd"
        case "in":
            return f"{startingMeasurement} is {feet*12}in"
        case "mi":
            return f"{startingMeasurement} is {feet/5280}mi"
        case _:
            return f"Invalid target unit: {targetUnit}"

# table of lambdas to convert a weight to grams 
toGrams = {
    # Metric units
    "g": lambda x: x,  # base unit
    "kg": lambda x: x * 1000,
    "mg": lambda x: x / 1000,
    "µg": lambda x: x / 1000000,
    "ug": lambda x: x / 1000000,  # alternative micro symbol
    "ng": lambda x: x / 1000000000,
    
    # Imperial units
    "lb": lambda x: x * 453.59237,  # pounds
    "lbs": lambda x: x * 453.59237,
    "oz": lambda x: x * 28.349523125,  # ounces
    "st": lambda x: x * 6350.29318,  # stone
    "ton": lambda x: x * 907184.74,  # US ton
    "tonne": lambda x: x * 1000000,  # metric ton
}

# table of lambdas to convert grams to a weight
fromGrams = {
    # Metric units
    "g": lambda x: x,  # base unit
    "kg": lambda x: x / 1000,
    "mg": lambda x: x * 1000,
    "µg": lambda x: x * 1000000,
    "ug": lambda x: x * 1000000,  # alternative micro symbol
    "ng": lambda x: x * 1000000000,
    
    # Imperial units
    "lb": lambda x: x / 453.59237,  # pounds
    "lbs": lambda x: x / 453.59237,
    "oz": lambda x: x / 28.349523125,  # ounces
    "st": lambda x: x / 6350.29318,  # stone
    "ton": lambda x: x / 907184.74,  # US ton
    "tonne": lambda x: x / 1000000,  # metric ton
}

# convert weight
def convertWeight(text: list):
    startingMeasurement = text[0]
    targetUnit = text[1] if len(text) > 1 else "g"  # default to grams if no target specified
    
    # Match pattern: number followed by unit (e.g., "2lb", "1.5kg", "1000mg")
    pattern = r'^(\d*\.?\d+)([a-zA-Zµ]+)$'
    
    match = re.match(pattern, startingMeasurement.lower())
    if not match:
        return "Invalid measurement format. Please use format like: 1.5kg, 2lb, 1000mg, etc."
    
    number = float(match.group(1))
    unit = match.group(2)
    
    # Convert to grams first
    if unit not in toGrams:
        return f"Invalid unit: {unit}. Supported units are: {', '.join(toGrams.keys())}"
    
    grams = toGrams[unit](number)
    
    # Convert to target unit
    if targetUnit not in fromGrams:
        return f"Invalid target unit: {targetUnit}. Supported units are: {', '.join(fromGrams.keys())}"
    
    result = fromGrams[targetUnit](grams)
    
    # Format the output with appropriate precision
    if abs(result) < 0.000001:  # For very small numbers
        formatted_result = f"{result:.10g}"
        #formatted_result = f"{result:g}e-10" experiment with scientific notation later
    elif abs(result) < 0.01:  # For small numbers
        formatted_result = f"{result:.6g}"
    else:  # For normal numbers
        formatted_result = f"{result:.2f}"
    
    return f"{startingMeasurement} is {formatted_result}{targetUnit}"

toLiters = {
    # Metric units
    "l": lambda x: x,  # base unit
    "ml": lambda x: x / 1000,
    "cl": lambda x: x / 100,
    "dl": lambda x: x / 10,
    "kl": lambda x: x * 1000,
    "µl": lambda x: x / 1000000,
    "ul": lambda x: x / 1000000,  # alternative micro symbol
    
    # Imperial units
    "gal": lambda x: x * 3.78541,  # US gallon
    "qt": lambda x: x * 0.946353,  # US quart
    "pt": lambda x: x * 0.473176,  # US pint
    "floz": lambda x: x * 0.0295735,  # US fluid ounce
    "cup": lambda x: x * 0.236588,  # US cup
    "tbsp": lambda x: x * 0.0147868,  # US tablespoon
    "tsp": lambda x: x * 0.00492892,  # US teaspoon
    "in3": lambda x: x * 0.0163871,  # cubic inch
    "ft3": lambda x: x * 28.3168,  # cubic foot
    "yd3": lambda x: x * 764.555,  # cubic yard
}

fromLiters = {
    # Metric units
    "l": lambda x: x,  # base unit
    "ml": lambda x: x * 1000,
    "cl": lambda x: x * 100,
    "dl": lambda x: x * 10,
    "kl": lambda x: x / 1000,
    "µl": lambda x: x * 1000000,
    "ul": lambda x: x * 1000000,  # alternative micro symbol
    
    # Imperial units
    "gal": lambda x: x / 3.78541,  # US gallon
    "qt": lambda x: x / 0.946353,  # US quart
    "pt": lambda x: x / 0.473176,  # US pint
    "floz": lambda x: x / 0.0295735,  # US fluid ounce
    "cup": lambda x: x / 0.236588,  # US cup
    "tbsp": lambda x: x / 0.0147868,  # US tablespoon
    "tsp": lambda x: x / 0.00492892,  # US teaspoon
    "in3": lambda x: x / 0.0163871,  # cubic inch
    "ft3": lambda x: x / 28.3168,  # cubic foot
    "yd3": lambda x: x / 764.555,  # mmm yesss cubic yard my favorite volume measurement???
}

def convertVolume(text:list) -> str:
    startingMeasurement = text[0]
    # okay. yes. i know that lowercase l is _technically_ lumens BUT i'm not implementing every single sig fig here blah blah blah
    # like most ppl are lazy with conversions n shi sooooo
    # and also whos gonna be converting like lumens to electronvolts like im not gonna do that shi
    targetUnit = text[1] if len(text) > 1 else "l"  # default to liters if no target specified
    
    # Match pattern: number followed by unit (e.g., "2gal", "1.5l", "1000ml")
    pattern = r'^(\d*\.?\d+)([a-zA-Zµ0-9]+)$'
    
    match = re.match(pattern, startingMeasurement.lower())
    if not match:
        return "Invalid measurement format. Please use format like: 1.5l, 2gal, 1000ml, etc."
    
    number = float(match.group(1))
    unit = match.group(2)
    
    # Convert to liters first
    if unit not in toLiters:
        return f"Invalid unit: {unit}. Supported units are: {', '.join(toLiters.keys())}"
    
    liters = toLiters[unit](number)
    
    # Convert to target unit
    if targetUnit not in fromLiters:
        return f"Invalid target unit: {targetUnit}. Supported units are: {', '.join(fromLiters.keys())}"
    
    result = fromLiters[targetUnit](liters)
    
    # Format the output with appropriate precision
    if abs(result) < 0.000001:  # For very small numbers
        formatted_result = f"{result:.10g}"
    elif abs(result) < 0.01:  # For small numbers
        formatted_result = f"{result:.6g}"
    else:  # For normal numbers
        formatted_result = f"{result:.2f}"
    
    return f"{startingMeasurement} is {formatted_result}{targetUnit}"

# table of lambdas to convert a time to seconds
toSeconds = {
    # Base unit
    "s": lambda x: x,  # seconds
    
    # Metric prefixes
    "ms": lambda x: x / 1000,  # milliseconds
    "µs": lambda x: x / 1000000,  # microseconds
    "us": lambda x: x / 1000000,  # alternative micro symbol
    "ns": lambda x: x / 1000000000,  # nanoseconds
    "ps": lambda x: x / 1000000000000,  # picoseconds
    
    # Larger units
    "min": lambda x: x * 60,  # minutes
    "h": lambda x: x * 3600,  # hours
    "d": lambda x: x * 86400,  # days
    "w": lambda x: x * 604800,  # weeks
    "mo": lambda x: x * 2592000,  # months (30 days)
    "y": lambda x: x * 31536000,  # years (365 days)
    
    # Special units
    "decade": lambda x: x * 315360000,  # decades
    "century": lambda x: x * 3153600000,  # centuries
    "millennium": lambda x: x * 31536000000,  # millennia
}

# table of lambdas to convert seconds to a time
fromSeconds = {
    # Base unit
    "s": lambda x: x,  # seconds
    
    # Metric prefixes
    "ms": lambda x: x * 1000,  # milliseconds
    "µs": lambda x: x * 1000000,  # microseconds
    "us": lambda x: x * 1000000,  # alternative micro symbol
    "ns": lambda x: x * 1000000000,  # nanoseconds
    "ps": lambda x: x * 1000000000000,  # picoseconds
    
    # Larger units
    "min": lambda x: x / 60,  # minutes
    "h": lambda x: x / 3600,  # hours
    "d": lambda x: x / 86400,  # days
    "w": lambda x: x / 604800,  # weeks
    "mo": lambda x: x / 2592000,  # months (30 days)
    "y": lambda x: x / 31536000,  # years (365 days)
    
    # Special units
    "decade": lambda x: x / 315360000,  # decades
    "century": lambda x: x / 3153600000,  # centuries
    "millennium": lambda x: x / 31536000000,  # millennia
}

def convertTimeMeasurement(text: list) -> str:
    startingMeasurement = text[0]
    targetUnit = text[1] if len(text) > 1 else "s"  # default to seconds if no target specified
    
    # Match pattern: number followed by unit (e.g., "2h", "1.5min", "1000ms")
    pattern = r'^(\d*\.?\d+)([a-zA-Zµ]+)$'
    
    match = re.match(pattern, startingMeasurement.lower())
    if not match:
        return "Invalid measurement format. Please use format like: 1.5h, 2min, 1000ms, etc."
    
    number = float(match.group(1))
    unit = match.group(2)
    
    # Convert to seconds first
    if unit not in toSeconds:
        return f"Invalid unit: {unit}. Supported units are: {', '.join(toSeconds.keys())}"
    
    seconds = toSeconds[unit](number)
    
    # Convert to target unit
    if targetUnit not in fromSeconds:
        return f"Invalid target unit: {targetUnit}. Supported units are: {', '.join(fromSeconds.keys())}"
    
    result = fromSeconds[targetUnit](seconds)
    
    # Format the output with appropriate precision
    if abs(result) < 0.000001:  # For very small numbers
        formatted_result = f"{result:.10g}"
    elif abs(result) < 0.01:  # For small numbers
        formatted_result = f"{result:.6g}"
    else:  # For normal numbers
        formatted_result = f"{result:.2f}"
    
    return f"{startingMeasurement} is {formatted_result}{targetUnit}"

def parse_time(time_str: str) -> Optional[datetime]:
    """Parse time string in various formats."""
    time_str = time_str.lower().strip()
    
    # Common time formats
    formats = [
        # Time only formats
        "%I:%M%p",  # 6:30am
        "%I%p",     # 6am
        "%I:%M",    # 6:30
        "%H:%M",    # 18:30
        "%H:%M:%S", # 18:30:00
        
        # Date and time formats
        "%I:%M%p %B %d, %Y",  # 6:30am June 6, 2025
        "%I:%M%p %B %d %Y",   # 6:30am June 6 2025
        "%I:%M%p %b %d, %Y",  # 6:30am Jun 6, 2025
        "%I:%M%p %b %d %Y",   # 6:30am Jun 6 2025
        "%I:%M%p %d %B %Y",   # 6:30am 6 June 2025
        "%I:%M%p %d %b %Y",   # 6:30am 6 Jun 2025
        "%I:%M%p %m/%d/%Y",   # 6:30am 06/06/2025
        "%I:%M%p %d/%m/%Y",   # 6:30am 06/06/2025
        
        # Date formats without time
        "%B %d, %Y",  # June 6, 2025
        "%B %d %Y",   # June 6 2025
        "%b %d, %Y",  # Jun 6, 2025
        "%b %d %Y",   # Jun 6 2025
        "%d %B %Y",   # 6 June 2025
        "%d %b %Y",   # 6 Jun 2025
        "%m/%d/%Y",   # 06/06/2025
        "%d/%m/%Y",   # 06/06/2025
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    
    return None

def convertDate(text: list) -> str:
    if len(text) < 2:
        return "Please provide both time and timezone. Example: 6:30am PST CST or 7:22am June 6, 2025 PST CST"
    
    # Join all parts except the last two (timezones) to handle dates with spaces
    time_parts = text[:-2]
    time_str = " ".join(time_parts)
    from_tz = text[-2].upper()
    to_tz = text[-1].upper()
    
    # Parse the time
    time = parse_time(time_str)
    if not time:
        return "Invalid time format. Please use formats like: 6:30am, 6am, 18:30, or 7:22am June 6, 2025"
    
    # Get timezone objects
    try:
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
    except pytz.exceptions.UnknownTimeZoneError as e:
        return f"Invalid timezone: {str(e)}. Please use valid timezone abbreviations (e.g., PST, EST, UTC)."
    
    # Localize the time to the source timezone
    try:
        localized_time = from_zone.localize(time)
    except ValueError:
        # If time is ambiguous (during DST transitions), use the first occurrence
        localized_time = from_zone.localize(time, is_dst=True)
    
    # Convert to target timezone
    converted_time = localized_time.astimezone(to_zone)
    
    # Format the output based on whether a date was provided
    if any(c.isdigit() for c in time_str.split()[-1]):  # Check if last part contains a year
        time_format = "%I:%M %p %B %d, %Y %Z"  # e.g., "06:30 AM June 6, 2025 PST"
    else:
        time_format = "%I:%M %p %Z"  # e.g., "06:30 AM PST"
    
    return f"{time_str} {from_tz} is {converted_time.strftime(time_format)}"

@app.command("/converttime")
def convert_time(ack, respond, command):
    # Acknowledge command request
    ack()
    text = command['text'].lower()
    content = text.split(" ")
    respond(convertDate(content))

@app.command("/convertunit")
def convert_units(ack, respond, command):
    # Acknowledge command request
    ack()
    text = command['text'].lower()
    supportedMeasurements = ["temp","temperature","length","distance","mass","weight","amount", "volume", "time"]
    measurement = text.split(" ")[0] # i dont actually use this but im too scared to delete it
    content = text.split(" ")[1:] # this should look something like "2lb kg"
    if text.startswith("temp") or text.startswith("temperature"):
        respond(convertTemp(content))
    elif text.startswith("length") or text.startswith("distance"):
        respond(convertLength(content))
    elif text.startswith("mass") or text.startswith("weight"):
        respond(convertWeight(content))
    elif text.startswith("amount") or text.startswith("volume"):
        respond(convertVolume(content))
    elif text.startswith("time"):
        respond(convertTimeMeasurement(content))
    else:
        respond(f"I'm sorry, but I don't know how to convert {text[1]}. Supported measurements are {', '.join(supportedMeasurements)}")




# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


