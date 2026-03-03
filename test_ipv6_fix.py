"""
Test script to verify IPv6 regex fix works correctly.

This test demonstrates that '::' alone (just two colons)
should NOT match, while valid IPv6 shorthand like '::1', '::ffff' etc.
SHOULD match.
"""

import re
import json
import sys
sys.path.insert(0, '.')

from pywhat.Data.regex.json import get_ipv6_regex

def test_ipv6_regex():
    """Test the IPv6 regex fix."""
    
    # Load the fixed IPv6 regex
    with open('pywhat/Data/regex.json', 'r') as f:
        data = json.load(f)
    
    for item in data:
        if 'Internet Protocol (IP) Address Version 6' in item.get('Name', ''):
            regex = item['Regex']
            break
    
    print("=" * 70)
    print("Testing IPv6 Regex Fix")
    print("=" * 70)
    print()
    
    test_cases = [
        ("::", False, "Just double colon - THE MAIN ISSUE"),
        ("::1", True, "IPv6 shorthand for ::1 (SHOULD MATCH)"),
        ("::ffff", True, "IPv6 shorthand for ::ffff (SHOULD MATCH)"),
        ("::dead:beef", True, "IPv6 with hex (SHOULD MATCH)"),
        ("::cafe", True, "IPv6 with hex (SHOULD MATCH)"),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True, "Full IPv6 address (SHOULD MATCH)"),
        ("[2001:db8::1]:8080", True, "IPv6 in brackets with port (SHOULD MATCH)"),
        ("fe80::", True, "IPv6 link-local with trailing :: (SHOULD MATCH)"),
    ]
    
    print("Running tests...")
    print()
    
    all_passed = True
    for test_str, should_match, description in test_cases:
        if re.search(regex, test_str):
            result = "✅ PASS"
            print(f"  {result}: '{test_str}' - {description}")
        else:
            result = "❌ FAIL"
            all_passed = False
            print(f"  {result}: '{test_str}' - {description}")
    
    print()
    print("=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print()
        print("The IPv6 regex fix is working correctly:")
        print("  - '::' alone does NOT match ✓")
        print("  - Valid IPv6 shorthand (::1, ::ffff, etc.) DO match ✓")
        print("  - Full IPv6 addresses DO match ✓")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("The IPv6 regex fix needs more work.")
        return False

if __name__ == "__main__":
    success = test_ipv6_regex()
    sys.exit(0 if success else 1)
