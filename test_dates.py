# unit tests for dates. 
import unittest
from datetime import datetime
import pytz
from main import convertDate, parse_time

class TestDateConversion(unittest.TestCase):
    def test_time_only_formats(self):
        # Test various time-only formats
        test_cases = [
            (["6:30am", "PST", "CST"], "6:30am PST is 08:30 AM CST"),
            (["6am", "EST", "UTC"], "6am EST is 11:00 AM UTC"),
            (["18:30", "GMT", "PST"], "18:30 GMT is 10:30 AM PST"),
            (["18:30:00", "UTC", "EST"], "18:30:00 UTC is 01:30 PM EST"),
        ]
        
        for input_args, expected in test_cases:
            with self.subTest(input_args=input_args):
                result = convertDate(input_args)
                self.assertEqual(result, expected)

    def test_date_time_formats(self):
        # Test various date-time formats
        test_cases = [
            (["7:22am", "June", "6,", "2025", "PST", "EST"], 
             "7:22am June 6, 2025 PST is 10:22 AM June 6, 2025 EST"),
            (["3:45pm", "15/06/2025", "GMT", "UTC"], 
             "3:45pm 15/06/2025 GMT is 03:45 PM 15/06/2025 UTC"),
            (["9:00am", "Jun", "6,", "2025", "CST", "PST"], 
             "9:00am Jun 6, 2025 CST is 07:00 AM Jun 6, 2025 PST"),
        ]
        
        for input_args, expected in test_cases:
            with self.subTest(input_args=input_args):
                result = convertDate(input_args)
                self.assertEqual(result, expected)

    def test_date_only_formats(self):
        # Test date-only formats (should default to midnight)
        test_cases = [
            (["June", "6,", "2025", "PST", "EST"], 
             "June 6, 2025 PST is 03:00 AM June 6, 2025 EST"),
            (["15/06/2025", "GMT", "UTC"], 
             "15/06/2025 GMT is 12:00 AM 15/06/2025 UTC"),
        ]
        
        for input_args, expected in test_cases:
            with self.subTest(input_args=input_args):
                result = convertDate(input_args)
                self.assertEqual(result, expected)

    def test_invalid_inputs(self):
        # Test invalid inputs
        test_cases = [
            (["6:30am"], "Please provide both time and timezone. Example: 6:30am PST CST or 7:22am June 6, 2025 PST CST"),
            (["invalid_time", "PST", "CST"], "Invalid time format. Please use formats like: 6:30am, 6am, 18:30, or 7:22am June 6, 2025"),
            (["6:30am", "INVALID_TZ", "CST"], "Invalid timezone: 'INVALID_TZ'. Please use valid timezone abbreviations (e.g., PST, EST, UTC)."),
        ]
        
        for input_args, expected in test_cases:
            with self.subTest(input_args=input_args):
                result = convertDate(input_args)
                self.assertEqual(result, expected)

    def test_dst_transitions(self):
        # Test DST transition times
        test_cases = [
            # Spring forward (March)
            (["2:30am", "March", "10,", "2024", "EST", "CST"], 
             "2:30am March 10, 2024 EST is 01:30 AM March 10, 2024 CST"),
            # Fall back (November)
            (["1:30am", "November", "3,", "2024", "EST", "CST"], 
             "1:30am November 3, 2024 EST is 12:30 AM November 3, 2024 CST"),
        ]
        
        for input_args, expected in test_cases:
            with self.subTest(input_args=input_args):
                result = convertDate(input_args)
                self.assertEqual(result, expected)

    def test_parse_time_function(self):
        # Test the parse_time helper function directly
        test_cases = [
            ("6:30am", datetime.strptime("6:30am", "%I:%M%p")),
            ("6am", datetime.strptime("6am", "%I%p")),
            ("18:30", datetime.strptime("18:30", "%H:%M")),
            ("7:22am June 6, 2025", datetime.strptime("7:22am June 6, 2025", "%I:%M%p %B %d, %Y")),
            ("3:45pm 15/06/2025", datetime.strptime("3:45pm 15/06/2025", "%I:%M%p %d/%m/%Y")),
            ("June 6, 2025", datetime.strptime("June 6, 2025", "%B %d, %Y")),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = parse_time(input_str)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        # Test edge cases
        test_cases = [
            # Year boundary
            (["11:59pm", "December", "31,", "2024", "PST", "EST"], 
             "11:59pm December 31, 2024 PST is 02:59 AM January 1, 2025 EST"),
            # Leap year
            (["11:59pm", "February", "29,", "2024", "PST", "EST"], 
             "11:59pm February 29, 2024 PST is 02:59 AM March 1, 2024 EST"),
            # Timezone with large offset
            (["12:00pm", "UTC", "NZST"], 
             "12:00pm UTC is 12:00 AM NZST"),
        ]
        
        for input_args, expected in test_cases:
            with self.subTest(input_args=input_args):
                result = convertDate(input_args)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main() 