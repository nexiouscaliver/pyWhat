"""
Test cases for IPv6 address identification.

Tests for issue #201: IPv6 regex should not match on '::' alone.
"""

from pywhat import identifier


r = identifier.Identifier()


def test_ipv6_rejects_lone_double_colon():
    """Verify that '::' alone is NOT identified as IPv6 (issue #201)."""
    out = r.identify("::")
    # No matches should be returned
    assert out["Regexes"] is None, ":: should not match any regex patterns"


def test_ipv6_matches_loopback():
    """Verify that '::1' is correctly identified as IPv6."""
    out = r.identify("::1")
    assert out["Regexes"] is not None
    matches = out["Regexes"]["text"]
    ipv6_matches = [m for m in matches if "IPv6" in m["Regex Pattern"]["Name"]]
    assert len(ipv6_matches) > 0, "::1 should match as IPv6"


def test_ipv6_matches_compressed_addresses():
    """Verify various compressed IPv6 addresses are matched."""
    test_addresses = [
        "2001:db8::1",
        "fe80::1",
        "2001::",
    ]
    
    for address in test_addresses:
        out = r.identify(address)
        assert out["Regexes"] is not None, f"{address} should match"
        matches = out["Regexes"]["text"]
        ipv6_matches = [m for m in matches if "IPv6" in m["Regex Pattern"]["Name"]]
        assert len(ipv6_matches) > 0, f"{address} should match as IPv6"


def test_ipv6_matches_full_address():
    """Verify full IPv6 addresses are matched."""
    full_address = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    out = r.identify(full_address)
    assert out["Regexes"] is not None
    matches = out["Regexes"]["text"]
    ipv6_matches = [m for m in matches if "IPv6" in m["Regex Pattern"]["Name"]]
    assert len(ipv6_matches) > 0, f"{full_address} should match as IPv6"


def test_ipv6_rejects_invalid_formats():
    """Verify invalid IPv6 formats are rejected."""
    invalid_addresses = [
        "::",  # Lone double colon (issue #201)
        "::::",  # Multiple double colons
    ]
    
    for address in invalid_addresses:
        out = r.identify(address)
        # These should not match as IPv6
        if out["Regexes"] is not None:
            matches = out["Regexes"]["text"]
            ipv6_matches = [m for m in matches if "IPv6" in m["Regex Pattern"]["Name"]]
            assert len(ipv6_matches) == 0, \
                f"{address} should not match as IPv6"
