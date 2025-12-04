# utils/astro.py

import swisseph as swe
from datetime import datetime, timezone, timedelta
import pytz

# Use Lahiri ayanamsa
swe.set_sid_mode(swe.SIDM_LAHIRI)

def jd_from_local(dt_local: datetime, tz_name: str):
    """
    Convert local datetime to Julian Day (UT).
    """
    tz = pytz.timezone(tz_name)
    if dt_local.tzinfo is None:
        dt_local = tz.localize(dt_local)
    dt_utc = dt_local.astimezone(pytz.utc)

    return swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600,
    )

def get_planet_longitudes(dt_local: datetime, tz_name: str, lat=0.0, lon=0.0):
    """
    Returns dict of planet longitudes + Ascendant + House cusps
    """
    jd = jd_from_local(dt_local, tz_name)

    planets = {
        'SUN': swe.SUN,
        'MOON': swe.MOON,
        'MARS': swe.MARS,
        'MERCURY': swe.MERCURY,
        'JUPITER': swe.JUPITER,
        'VENUS': swe.VENUS,
        'SATURN': swe.SATURN,
        'RAHU': swe.MEAN_NODE,
        'KETU': swe.MEAN_NODE,   # Ketu = 180° opposite Rahu
    }

    res = {}

    # Planet longitudes
    for name, pid in planets.items():
        pos = swe.calc_ut(jd, pid)
        lon_deg = pos[0] % 360.0
        res[name] = round(lon_deg, 6)

    # Correct Ketu longitude
    res['KETU'] = (res['RAHU'] + 180) % 360

    # Ascendant & Houses
    try:
        cusps, ascmc = swe.houses(jd, lat, lon, b'P')
        res['ASC'] = round(ascmc[0] % 360.0, 6)

        for i in range(1, 13):
            res[f'CUSP_{i}'] = round(cusps[i-1] % 360.0, 6)

    except:
        res['ASC'] = None

    return res


def nakshatra_from_long(lon):
    """
    Returns (Nakshatra number 1-27, Pada 1-4)
    """
    size = 360.0 / 27.0  # 13°20'
    nak = int((lon % 360.0) / size) + 1

    # Pada
    inside = (lon % size) / size
    pada = int(inside * 4) + 1

    return nak, pada


def simple_chart_report(dt_iso, tz_name='Asia/Kolkata', lat=29.97, lon=77.55):
    """
    Main function: returns Moon Nakshatra, Ascendant, All planets
    """
    if isinstance(dt_iso, str):
        dt = datetime.fromisoformat(dt_iso)
    else:
        dt = dt_iso

    planets = get_planet_longitudes(dt, tz_name, lat, lon)

    moon_lon = planets['MOON']
    nak, pada = nakshatra_from_long(moon_lon)

    report = {
        "moon_long": moon_lon,
        "nakshatra": nak,
        "pada": pada,
        "ascendant": planets.get("ASC"),
        "planets": planets
    }

    return report
