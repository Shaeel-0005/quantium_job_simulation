from app import app

def test_header_present(dash_duo):
    dash_duo.start_server(app)
    # Updated selector for the new h1 title
    dash_duo.wait_for_element("h1.title", timeout=10)
    assert "PINK MORSELS" in dash_duo.find_element("h1.title").text

def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    # Plotly graph class remains unchanged
    dash_duo.wait_for_element(".js-plotly-plot", timeout=10)

def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    # Updated to match the custom region toggle container
    dash_duo.wait_for_element(".region-toggle", timeout=10)
    # Verify all 5 options rendered correctly
    options = dash_duo.find_elements(".region-option")
    assert len(options) == 5