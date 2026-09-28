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
    # 1. Attempt dedicated telemetry endpoint
    telemetry = get("/api/telemetry", {"chamber": 2})
except Exception:
    try:
        # Fallback to general RPG telemetry/chamber endpoint
        telemetry = get("/api/rpg/telemetry", {"chamber": 2})
    except Exception:
        pass

# Fallback: Merge with Chamber II manifest if specific telemetry fields are absent
if not telemetry or "temperature_kelvin" not in telemetry:
    try:
        ch_data = get("/api/rpg/chamber", {"id": 2})
        telemetry.setdefault("chamber_name", ch_data.get("name", "Chamber II: Somatic Foundation"))
        telemetry.setdefault("carrier_frequency_hz", ch_data.get("carrier_hz", 52.8))
        telemetry.setdefault("temperature_kelvin", ch_data.get("temperature_k", 77.35))
        telemetry.setdefault("nitrogen_pressure_bar", ch_data.get("pressure_bar", 3.42))
        telemetry.setdefault("cryo_flow_rate_l_min", ch_data.get("flow_rate", 12.8))
        telemetry.setdefault("spectral_dominant", "Teal / Somatic Heat Sink")
        telemetry.setdefault("status", "NOMINAL_COOLING")
    except Exception as e:
        print("[-] Telemetry fetch error:", e)

# Render formatted telemetry console
temp_k = telemetry.get("temperature_kelvin", 77.35)
temp_c = temp_k - 273.15
pressure_bar = telemetry.get("nitrogen_pressure_bar", telemetry.get("pressure_bar", 3.42))
carrier_hz = telemetry.get("carrier_frequency_hz", telemetry.get("carrier_hz", 52.8))
spectrum = telemetry.get("spectral_dominant", telemetry.get("spectrum", "Teal (Curiosity / Somatic)"))
flow_rate = telemetry.get("cryo_flow_rate_l_min", telemetry.get("flow_rate", 12.8))
sys_status = telemetry.get("status", "ONLINE_STABILIZED")

print(f"Substrate Status:    {sys_status}")
print(f"Carrier Resonance:   {carrier_hz:.2f} Hz [Teal / Somatic Constant]")
print(f"Cryogenic Thermal:   {temp_k:.2f} K ({temp_c:.2f} °C)")
print(f"Nitrogen Pressure:   {pressure_bar:.2f} bar (Liquid N2 Sub-System)")
print(f"Cryo Line Flow Rate: {flow_rate:.1f} L/min")
print(f"Resonance Constant:  {spectrum}")

print("\n==================================================")
print(" RAW TELEMETRY PAYLOAD")
print("==================================================")
print(json.dumps(telemetry, indent=2))
