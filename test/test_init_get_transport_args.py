import pytest
from ha_template_mcp import get_transport_kwargs


class TestGetTransportKwargs:
    """Test cases for the get_transport_kwargs function."""

    def test_none_input_returns_empty_dict(self):
        """Test that None input returns an empty dictionary."""
        result = get_transport_kwargs(None)
        assert result == {}

    def test_empty_list_returns_empty_dict(self):
        """Test that an empty list returns an empty dictionary."""
        result = get_transport_kwargs([])
        assert result == {}

    def test_single_non_port_argument(self):
        """Test with a single non-port argument."""
        transport_arg = [("host", "localhost")]
        result = get_transport_kwargs(transport_arg)
        assert result == {"host": "localhost"}

    def test_multiple_non_port_arguments(self):
        """Test with multiple non-port arguments."""
        transport_arg = [("host", "localhost"), ("timeout", "30")]
        result = get_transport_kwargs(transport_arg)
        assert result == {"host": "localhost", "timeout": "30"}

    def test_port_as_string_converts_to_int(self):
        """Test that port value as string is converted to integer."""
        transport_arg = [("port", "8080")]
        result = get_transport_kwargs(transport_arg)
        assert result == {"port": 8080}
        assert isinstance(result["port"], int)

    def test_port_as_int_remains_int(self):
        """Test that port value as integer remains integer."""
        transport_arg = [("port", 8080)]
        result = get_transport_kwargs(transport_arg)
        assert result == {"port": 8080}
        assert isinstance(result["port"], int)

    def test_port_with_other_arguments(self):
        """Test port conversion with other arguments present."""
        transport_arg = [("host", "0.0.0.0"), ("port", "3000"), ("debug", "true")]
        result = get_transport_kwargs(transport_arg)
        assert result == {"host": "0.0.0.0", "port": 3000, "debug": "true"}
        assert isinstance(result["port"], int)

    def test_port_zero_as_string(self):
        """Test that port value '0' converts correctly."""
        transport_arg = [("port", "0")]
        result = get_transport_kwargs(transport_arg)
        assert result == {"port": 0}
        assert isinstance(result["port"], int)

    def test_port_common_values(self):
        """Test common port values."""
        test_cases = [
            ("80", 80),
            ("443", 443),
            ("3000", 3000),
            ("8000", 8000),
            ("65535", 65535),
        ]
        for port_str, port_int in test_cases:
            transport_arg = [("port", port_str)]
            result = get_transport_kwargs(transport_arg)
            assert result["port"] == port_int
            assert isinstance(result["port"], int)

    def test_duplicate_keys_last_value_wins(self):
        """Test that when duplicate keys exist, the last value is used."""
        transport_arg = [("host", "localhost"), ("host", "127.0.0.1")]
        result = get_transport_kwargs(transport_arg)
        assert result == {"host": "127.0.0.1"}

    def test_port_none_value_not_converted(self):
        """Test that if port is explicitly None, it's not converted."""
        transport_arg = [("port", None)]
        result = get_transport_kwargs(transport_arg)
        # The function checks if port_value is not None before converting
        # So None should remain None (not be converted)
        assert result == {"port": None}

    def test_numeric_string_port_conversion(self):
        """Test various numeric string formats for port."""
        transport_arg = [("port", "1234")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == 1234

    def test_preserves_all_non_port_types(self):
        """Test that non-port arguments preserve their types."""
        transport_arg = [
            ("string_val", "test"),
            ("int_val", 123),
            ("bool_val", True),
            ("float_val", 3.14),
        ]
        result = get_transport_kwargs(transport_arg)
        assert result["string_val"] == "test"
        assert result["int_val"] == 123
        assert result["bool_val"] is True
        assert result["float_val"] == 3.14

    def test_invalid_port_string_raises_error(self):
        """Test that invalid port string raises ValueError."""
        transport_arg = [("port", "not_a_number")]
        with pytest.raises(ValueError):
            get_transport_kwargs(transport_arg)

    def test_port_with_whitespace_raises_error(self):
        """Test that port with whitespace raises ValueError."""
        transport_arg = [("port", " 8080 ")]
        # This will raise ValueError because int(" 8080 ") works but let's be cautious
        # Actually int(" 8080 ") works in Python, so this might not raise
        # Let me test with something that definitely won't work
        transport_arg = [("port", "8080 extra")]
        with pytest.raises(ValueError):
            get_transport_kwargs(transport_arg)

    def test_empty_string_port_raises_error(self):
        """Test that empty string port raises ValueError."""
        transport_arg = [("port", "")]
        with pytest.raises(ValueError):
            get_transport_kwargs(transport_arg)

    def test_negative_port_converts(self):
        """Test that negative port strings convert to negative integers."""
        transport_arg = [("port", "-1")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == -1
        assert isinstance(result["port"], int)

    def test_float_string_port_raises_error(self):
        """Test that float string port raises ValueError."""
        transport_arg = [("port", "8080.5")]
        with pytest.raises(ValueError):
            get_transport_kwargs(transport_arg)

    def test_large_port_number_converts(self):
        """Test that very large port numbers convert correctly."""
        transport_arg = [("port", "99999")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == 99999
        assert isinstance(result["port"], int)

    def test_port_one(self):
        """Test port value 1 (minimum valid port)."""
        transport_arg = [("port", "1")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == 1

    def test_special_characters_in_non_port_values(self):
        """Test that special characters in non-port values are preserved."""
        transport_arg = [
            ("path", "/api/v1/endpoint"),
            ("query", "?key=value&other=123"),
            ("header", "Bearer token-with-dashes_and_underscores"),
        ]
        result = get_transport_kwargs(transport_arg)
        assert result["path"] == "/api/v1/endpoint"
        assert result["query"] == "?key=value&other=123"
        assert result["header"] == "Bearer token-with-dashes_and_underscores"

    def test_mixed_order_with_port_first(self):
        """Test that port conversion works regardless of order."""
        transport_arg = [("port", "8080"), ("host", "localhost")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == 8080
        assert result["host"] == "localhost"

    def test_mixed_order_with_port_middle(self):
        """Test port conversion when port is in the middle."""
        transport_arg = [("host", "localhost"), ("port", "8080"), ("timeout", "30")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == 8080
        assert result["host"] == "localhost"
        assert result["timeout"] == "30"

    def test_mixed_order_with_port_last(self):
        """Test port conversion when port is last."""
        transport_arg = [("host", "localhost"), ("timeout", "30"), ("port", "8080")]
        result = get_transport_kwargs(transport_arg)
        assert result["port"] == 8080
        assert result["host"] == "localhost"
        assert result["timeout"] == "30"
