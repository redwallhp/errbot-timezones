# Errbot Timezone Converter

## Usage
Set personal timezone: `!settz America/New_York`

Convert a time: `!tz <time> <from timezone> [to timezone]`

```
!tz 7:20 PM Australia/Brisbane
!tz 7:20 PM EST
!tz 7:20 PM UTC redwallhp
!tz 7:20 PM redwallhp UTC
```

Any user's registered timezone is accepted as a valid timezone format. If no "to timezone" is specified, your registered timezone will be used. If one is no set, UTC will be the fallback.
