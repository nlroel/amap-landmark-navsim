"""Simple local HTML visualization."""

from __future__ import annotations


def render_html(title: str = "Amap Landmark NavSim") -> str:
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head><meta charset=\"utf-8\"><title>{title}</title></head>
<body>
  <h1>{title}</h1>
  <p>GeoJSON artifacts: route.geojson, trace.geojson, events.geojson, landmarks.geojson</p>
  <div id=\"map\">Open the GeoJSON files in your preferred map viewer.</div>
</body>
</html>
"""
