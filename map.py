import streamlit as st

def map_image(location, zoom=12, size="600x400"):
    LOCATION_COORDS = {
    "Bath": (51.3811, -2.3590),
    "Brighton": (50.8225, -0.1372),
    "Cambridge": (52.2053, 0.1218),
    "Canterbury": (51.2802, 1.0789),
    "Chester": (53.1934, -2.8931),
    "Cornwall": (50.2660, -5.0527),
    "Cotswolds": (51.8330, -1.8433),
    "Devon": (50.7156, -3.5309),
    "Durham": (54.7753, -1.5849),
    "Edinburgh": (55.9533, -3.1883),
    "Exeter": (50.7184, -3.5339),
    "Glasgow": (55.8642, -4.2518),
    "Harrogate": (53.9921, -1.5418),
    "Harrogate, UK": (53.9921, -1.5418),
    "Inverness": (57.4778, -4.2247),
    "Lake District": (54.4609, -3.0886),
    "Norfolk": (52.6139, 0.8864),
    "Northumberland": (55.2083, -2.0784),
    "Oxford": (51.7520, -1.2577),
    "Peak District": (53.3400, -1.7900),
    "Scottish Highlands": (57.1200, -4.7100),
    "Stratford-upon-Avon": (52.1917, -1.7073),
    "Suffolk": (52.1872, 1.0039),
    "Windsor": (51.4839, -0.6044),
    "York": (53.9590, -1.0815),
}
    
    key = location

    if key not in LOCATION_COORDS:
        return "./Po_Profile_cropped.jpg"
    
    lat, lng = LOCATION_COORDS.get(key)

    return (
        "https://api.maptiler.com/maps/streets/static/"
        f"{lng},{lat},12/600x400.png"
        f"?key={st.secrets['MAPTILER_API_KEY']}"
    )
    
