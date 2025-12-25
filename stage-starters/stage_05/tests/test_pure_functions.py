import app.main as m


def test_clamp_int_below_min():
    assert m.clamp_int(0, 1, 10) == 1


def test_clamp_int_above_max():
    assert m.clamp_int(50, 1, 10) == 10


def test_clamp_int_in_range():
    assert m.clamp_int(5, 1, 10) == 5


def test_parse_latlon_comma_format():
    assert m.parse_latlon("47.6062,-122.3321") == (47.6062, -122.3321)


def test_parse_latlon_space_format():
    assert m.parse_latlon("47.6062 -122.3321") == (47.6062, -122.3321)


def test_parse_latlon_invalid_text():
    assert m.parse_latlon("hello") is None


def test_parse_latlon_out_of_bounds():
    assert m.parse_latlon("95,0") is None
    assert m.parse_latlon("0,200") is None


def test_normalize_us_location_converts_state_abbrev():
    assert m.normalize_us_location("Seattle,WA") == "Seattle, Washington"
    assert m.normalize_us_location("Portland,OR") == "Portland, Oregon"


def test_normalize_us_location_leaves_unknown_state():
    assert m.normalize_us_location("Seattle,XX") == "Seattle XX"


def test_normalize_us_location_no_comma_no_change():
    assert m.normalize_us_location("Seattle") == "Seattle"
