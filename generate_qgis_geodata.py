"""Generates the Trade Map's chokepoint exposure buffer rings and country-
to-chokepoint distance matrix using real QGIS (PyQGIS), not a
re-implementation of its math in another library.

Companion to the same approach shipped in this project's sibling, the Gulf
AI & Tech-Bloc Alignment Tracker (see that repo's
src/data_pipeline/generate_qgis_geodata.py) -- same two real QGIS engines,
applied here to this project's own 34 tracked MENASA economies
(COUNTRY_CAPITAL_COORDS) and 3 maritime chokepoints (MARITIME_CHOKEPOINTS,
geoeconomic_data.py), both already-existing, already-cited datasets. This
adds no new coordinates or facts -- it computes real geodesic geometry from
data already in this repo.

Offline/build-time step: output is checked into geodata/qgis_*.csv/geojson
and app.py just reads it, rather than requiring QGIS itself (roughly 1GB of
Qt/GDAL/GRASS dependencies) as a runtime dependency of a Streamlit app on
Render's free tier.

Two real QGIS engines, not approximated:
1. Distance matrix: QgsDistanceArea in ellipsoidal (WGS84) mode -- the same
   engine behind QGIS's own "Measure" tool.
2. Buffer rings: QgsGeometry.buffer() (the same GEOS-backed engine QGIS's
   own "native:buffer" processing algorithm calls), applied in a custom
   azimuthal-equidistant projection centered on each chokepoint, so the
   result is a true geodesic circle rather than a flat-projection
   approximation.

Requires QGIS installed with its Python bindings (`apt-get install qgis`
on Debian/Ubuntu). Run with the Python QGIS was built against -- on Ubuntu
24.04 with the qgis apt package, that's /usr/bin/python3.12:

    QT_QPA_PLATFORM=offscreen /usr/bin/python3.12 generate_qgis_geodata.py

Output (checked into the repo, so the deployed app never needs QGIS):
  geodata/qgis_country_chokepoint_distances.csv
  geodata/qgis_chokepoint_buffers.geojson
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from fetch_data import COUNTRIES
from geoeconomic_data import COUNTRY_CAPITAL_COORDS, MARITIME_CHOKEPOINTS

BUFFER_RADII_M = [250_000, 500_000, 1_000_000]
BUFFER_SEGMENTS = 18  # points per quarter-circle-equivalent -> 72-point rings
OUT_DIR = Path("geodata")


def main() -> None:
    from qgis.core import (
        QgsApplication,
        QgsCoordinateReferenceSystem,
        QgsCoordinateTransform,
        QgsDistanceArea,
        QgsGeometry,
        QgsPointXY,
        QgsProject,
    )

    OUT_DIR.mkdir(exist_ok=True)

    qgs = QgsApplication([], False)
    qgs.initQgis()

    try:
        # ---- 1. Distance matrix: QgsDistanceArea, ellipsoidal WGS84 ----
        da = QgsDistanceArea()
        da.setEllipsoid("WGS84")
        wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
        da.setSourceCrs(wgs84, QgsProject.instance().transformContext())

        distance_rows = []
        for iso3, (lat, lon) in COUNTRY_CAPITAL_COORDS.items():
            country_name = COUNTRIES.get(iso3, iso3)
            p1 = QgsPointXY(lon, lat)
            for cp_id, cp in MARITIME_CHOKEPOINTS.items():
                p2 = QgsPointXY(cp["lon"], cp["lat"])
                dist_km = da.measureLine(p1, p2) / 1000.0
                distance_rows.append(
                    {
                        "iso3": iso3,
                        "country": country_name,
                        "chokepoint_id": cp_id,
                        "chokepoint_name": cp["name"],
                        "distance_km": round(dist_km, 2),
                    }
                )

        out_csv = OUT_DIR / "qgis_country_chokepoint_distances.csv"
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["iso3", "country", "chokepoint_id", "chokepoint_name", "distance_km"])
            writer.writeheader()
            writer.writerows(distance_rows)
        print(f"Wrote {len(distance_rows)} distance rows to {out_csv}")

        # ---- 2. Buffer rings: QgsGeometry.buffer() in a local azimuthal-
        # equidistant CRS centered on each chokepoint, reprojected to WGS84.
        features = []
        for cp_id, cp in MARITIME_CHOKEPOINTS.items():
            lon, lat = cp["lon"], cp["lat"]
            aeqd_wkt = f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
            local_crs = QgsCoordinateReferenceSystem.fromProj(aeqd_wkt)
            to_local = QgsCoordinateTransform(wgs84, local_crs, QgsProject.instance())
            to_wgs84 = QgsCoordinateTransform(local_crs, wgs84, QgsProject.instance())

            center_local = to_local.transform(QgsPointXY(lon, lat))
            center_geom = QgsGeometry.fromPointXY(center_local)

            for radius_m in BUFFER_RADII_M:
                buffered = center_geom.buffer(radius_m, BUFFER_SEGMENTS)
                buffered.transform(to_wgs84)
                ring = buffered.asPolygon()[0]
                coords = [[pt.x(), pt.y()] for pt in ring]
                features.append(
                    {
                        "type": "Feature",
                        "properties": {
                            "chokepoint_id": cp_id,
                            "chokepoint_name": cp["name"],
                            "radius_km": radius_m / 1000,
                        },
                        "geometry": {"type": "Polygon", "coordinates": [coords]},
                    }
                )

        geojson = {"type": "FeatureCollection", "features": features}
        out_geojson = OUT_DIR / "qgis_chokepoint_buffers.geojson"
        with open(out_geojson, "w", encoding="utf-8") as f:
            json.dump(geojson, f)
        print(f"Wrote {len(features)} buffer ring features to {out_geojson}")

    finally:
        qgs.exitQgis()


if __name__ == "__main__":
    main()
