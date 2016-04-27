from errbot import BotPlugin, botcmd
import re, pytz, datetime
import tz_definitions

class Timezones(BotPlugin):


    def activate(self):
        super().activate()
        self.user_zones = self.get("USER_ZONES", {})
        self['USER_ZONES'] = self.user_zones


    @botcmd
    def settz(self, msg, args):
        you = msg.frm.person.replace('@', '')
        you = you.lower()
        if len(args) > 0:
            if args in pytz.common_timezones:
                self.user_zones[you] = args
                self['USER_ZONES'] = self.user_zones
                return "Updated your timezone"
            else:
                return "You must enter a valid timezone. e.g. America/New_York"
        else:
            return "Usage: settz America/New_York"


    @botcmd
    def tz(self, msg, args):
        """ Convert a timezone """
        if len(args) < 1:
            return "Usage: tz <time> <input timezone> [output timezone]"

        hour, minute, second, remainder = self.parse_time(args)
        zargs = remainder.split(' ')
        input_zone = self.parse_timezone(zargs[0])
        if len(zargs) > 1:
            output_zone = self.parse_timezone(zargs[1])
        else:
            output_zone = self.user_zones.get(msg.frm.person.replace('@', ''), 'UTC')
        original_time = "%s:%s" % (hour, minute)

        dt = datetime.datetime.today()
        dt = dt.replace(hour = hour, minute = minute, second = second)
        idt = pytz.timezone(input_zone).localize(dt)
        new_dt = idt.astimezone(pytz.timezone(output_zone))
        original_time = dt.strftime("%I:%M %p")
        new_time = new_dt.strftime("%I:%M %p")

        daydiff = ""
        delta = new_dt.day - dt.day
        if delta > 0:
            daydiff = " the next day"
        elif delta < 0:
            daydiff = " the previous day"

        yield "**%s** %s%s *(converted from %s %s)*" % (new_time, output_zone, daydiff, original_time, input_zone)


    def parse_time(self, text):
        regex = re.compile(r'([0-9]?[0-9]):([0-5][0-9])(:[0-5][0-9])?( PM| AM)?', re.I)
        hour = 0
        minute = 0
        second = 0
        match = regex.search(text)
        if match:
            hour = int(match.group(1))
            # convert to 24-hour format
            if str(match.group(4)).lower() == " pm":
                if hour != 12:
                    hour = hour + 12
            if str(match.group(4)).lower() == " am":
                if hour == 12:
                    hour = 0
            minute = int(match.group(2))
            if match.group(3):
                second = int(match.group(3)[1:])
        remainder = regex.sub('', text).strip()
        return hour, minute, second, remainder


    def parse_timezone(self, text):
        if text.lower() in tz_definitions.ABBREVIATIONS:
            return tz_definitions.ABBREVIATIONS.get(text.lower(), "UTC")
        elif text in pytz.common_timezones:
            return text
        elif text.lower() in self.user_zones:
            return self.user_zones[text.lower()]
        else:
            return "UTC"
