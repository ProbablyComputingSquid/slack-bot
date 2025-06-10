June 1st, 2025
7:19 pm: trying to set up correct slack permissions. looking through the slack docs. got all my tokens n stuff all set up
7:23 pm: just added event permissions per the startup guide
7:26 pm: yoinking more example code to try to figure out wtf is going on with these buttons, why is there so much JSON ahfwoifeoiwj
7:36 pm: set up my first slash command! /converttime 
7:36 pm: it actually doesnt work yet, it just echoes the text lmao. BUT we will make it work, trust!!!
7:37 pm: going to take a shower and a break. 
7:52 pm: the grind never ends. time to write converter functions for temperature first
8:24 pm: /convertunit temp works now!!! also theres more funny text responses because yes
8:34 pm: trying to make /convertlength work
June 2nd, 2025
10:56 am: brainstorming
1:10 pm: making /convertlength work hopefully
4:50 pm: had ai write me unit tests, thank you so much chatGPT :heart:
4:51 pm: oops miles are broken
4:53 pm: fixed miles
June 7th, 2025
~7am: began with the convertWeight method
took a break to do gig work
11:51 am: writing tests for convertWeight
12:15 pm: had cursor write me some test cases, turns out i was distinguishing from imperial and metric incorrectly :skull: 
i'll do better next time and be more careful. that's it for now. 
7:27 pm: starting on more conversions, this time liquid measurements
7:40 pm: convertVolume has been finished, the lambda setup is now so much more clean and readable
7:46 pm: absolutely loving this template i have, i can just get cursor to write the lambdas and copypaste the code
7:49 pm: guh
7:51 pm: I AM ACTUALLY SO COOKED I FORGOT TO PUSH EVERYTHING TO GITHUB
7:52 pm: bro its actually so over,,, im supposed to push hourly but i forgot to even push AT ALL IM SUCH an IDIOT aiugs
7:55 pm: trying to deploy to nest
7:55 pm: i forgot about .env variables
7:58 pm: wrote my systemctl files on nest, glad i remember how to do it (jk just copied my old ones and edited them)
7:58 pm: considered my bad coding practices
7:59 pm: forgot about .env variables again
8:00 pm: forgot about pip
8:04 pm: forgot about venv
8:05 pm: wrote requirements.txt
8:06 pn: LETS GO we got it running on slack, now time to make it BETTER
8:06 pm: nevermind we eep tonight, need to wake up bright and early mañana
June 9th, 2025: 
16:33 - time to setup cronjobs
16:43 - who cares about cronjobs when my code doesnt work :Despair:
16:48 -  diagnosed the problem, apparently it's using "true timezones" per the stackoverflow post https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones which i did not realize is different than timezone abbreviations
16:54 - made dates default to today instead of january 01, 1900
17:04 - added some more niche timezones, i guess the guam users (literally none) will be happy
17:12 - weh im fixing unit tests
17:12 - more coverage? or im adjusting unit tests to fit my outputs 
17:14 - timezones are so weird
17:25 im confused why is pytz telling me that times are off by like 4 minutes huh
17:47 - reading through block kit docs
17:50 - converthelp time, we using block kit for this one ig
