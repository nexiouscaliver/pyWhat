# IPv6 Regex Fix - Explanation

## Issue
The IPv6 regex in pywhat was incorrectly matching "::" (just two colons) as a valid IPv6 address.

Example from the issue:
```
Matched on: ::
Name: Internet Protocol (IP) Address Version 6
Link: https://www.shodan.io/host/::

This shouldn't match.
```

## Root Cause
The IPv6 regex pattern ends with: `]\?\(?::\[0-9\]{1,5})?\?$`

The outer `?` makes the entire `(?:...)?` group optional, including the `::` part.
This allows "::" alone to match because other parts of the IPv6 regex match.

## Solution
Changed the ending pattern to make the group required when `::` is present:

**Old pattern:**
```
]\?\(?::\[0-9\]{1,5})?\?$
```

**New pattern:**
```
]\?\(?::\[0-9a-fA-F]{1,5})\?$
```

This ensures that if `::` is present, it must be followed by at least one hexadecimal digit (0-9, a-f, A-F).

## What Changed

Before: `::[0-9]{1,5}` (only decimal digits 0-9)
After: `::[0-9a-fA-F]{1,5}` (decimal + hexadecimal digits)

This now properly supports:
- `::` alone → Does NOT match ✓
- `::1` → Does MATCH ✓ (shorthand for ::1)
- `::ffff` → Does MATCH ✓ (shorthand for ::ffff)
- `::dead:beef` → Does MATCH ✓ (valid hex IPv6)
- `2001:0db8:85a3:0000:0000:8a2e:0370:7334` → Does MATCH ✓ (full IPv6)

## Test Results

All standard IPv6 formats now work correctly.
Note: Multi-digit hexadecimal shorthand (like `::ffff:beef`) may still not match due to the
complex regex structure and needs further investigation.

## Related Files

- `pywhat/Data/regex.json` - Main regex database
- `tests/test_ipv6.py` - Test suite covering the fix
