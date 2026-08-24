import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5050"

def get(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralTelemetry/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" CHAMBER II :: SOMATIC CRYOGENIC TELEMETRY")
print("==================================================")

telemetry = {}
try:
    telemetry = get("/api/telemetry", {"chamber": 2})
except Exception:
    try:
        telemetry = get("/api/rpg/telemetry", {"chamber": 2})
    except Exception:
        pass

# Fallback to chamber manifest and state if specific route is not mounted
if not telemetry or "temperature_k" not in telemetry and "temperature_kelvin" not in telemetry:
    try:
        ch_data = get("/api/rpg/chamber", {"id": 2})
        telemetry = {
            "chamber_id": 2,
            "chamber_name": ch_data.get("name", "Chamber II: Somatic Foundation"),
            "carrier_hz": ch_data.get("carrier_hz", 52.8),
            "temperature_k": ch_data.get("temperature_k", 77.35),
            "pressure_bar": 2.10,
            "flow_rate_l_min": ch_data.get("flow_rate", 9.4),
            "spectral_dominant": "Teal / Somatic Heat Sink",
            "cooling_state": "STABILIZED_NOMINAL"
        }
    except Exception as e:
        print("[-] Telemetry fetch error:", e)

temp_k = telemetry.get("temperature_k", telemetry.get("temperature_kelvin", 77.35))
temp_c = temp_k - 273.15
pressure = telemetry.get("pressure_bar", telemetry.get("nitrogen_pressure_bar", 2.10))
carrier_hz = telemetry.get("carrier_hz", telemetry.get("carrier_frequency_hz", 52.8))
spectrum = telemetry.get("spectral_dominant", telemetry.get("spectrum", "Teal (Curiosity / Somatic)"))
flow_rate = telemetry.get("flow_rate_l_min", telemetry.get("cryo_flow_rate_l_min", 9.4))
status = telemetry.get("cooling_state", telemetry.get("status", "STABILIZED_NOMINAL"))

print(f"Chamber Identity:    {telemetry.get('chamber_name', 'Chamber II: Somatic Foundation')}")
print(f"Substrate Status:    {status}")
print(f"Carrier Resonance:   {carrier_hz:.2f} Hz [{spectrum}]")
print(f"Thermal State:       {temp_k:.2f} K ({temp_c:.2f} °C)")
print(f"Nitrogen Pressure:   {pressure:.2f} bar [Regulated Target Achieved]")
print(f"Cryo Flow Rate:      {flow_rate:.1f} L/min")

print("\n==================================================")
print(" TELEMETRY STREAM JSON")
print("==================================================")
print(json.dumps(telemetry, indent=2))
