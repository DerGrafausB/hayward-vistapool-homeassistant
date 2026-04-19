# Hayward VistaPool Home Assistant Integration

Custom integration for [Home Assistant](https://www.home-assistant.io) that connects your **Hayward VistaPool / PoolWatch WiFi module** to Home Assistant via Firebase + Firestore.

Developed by **Searise Developments Ltd.**  
License: MIT

---

## ✨ Features

### 🌡️ Pool Chemistry
- `sensor.vistapool_water_temperature` → Water Temperature (°C)  
- `sensor.vistapool_ph_current` → pH Current  
- `sensor.vistapool_ph_low_setpoint` → pH Low Setpoint  
- `sensor.vistapool_ph_high_setpoint` → pH High Setpoint  
- `sensor.vistapool_orp` → Oxidation Reduction Potential, measured/current (mV)  
- `sensor.vistapool_orp_setpoint` → ORP Setpoint (mV)  
- `sensor.vistapool_chlorine_status` → Chlorine Status (%)  
- `sensor.vistapool_salt_level` → Salt Level (%)  
- `sensor.vistapool_ph_tank_level` → pH Tank Level (%)  
- `sensor.vistapool_chlorine_tank_level` → Chlorine Tank Level (%)  
- `number.vistapool_orp_setpoint` → ORP Setpoint writable (mV)  
- `number.vistapool_ph_low_setpoint` → pH Low Setpoint writable  
- `number.vistapool_ph_high_setpoint` → pH High Setpoint writable  

### ⏱️ Equipment Runtime
- `sensor.vistapool_salt_cell_runtime_partial` → Salt Cell Runtime (Partial, h)  
- `sensor.vistapool_salt_cell_runtime_total` → Salt Cell Runtime (Total, h)  

### ⚙️ Filtration
- `sensor.vistapool_filtration_intel_temp` → Filtration Intel Temp (°C)  
- `sensor.vistapool_filtration_heating_temp` → Filtration Heating Temp (°C)  
- `sensor.vistapool_filtration_smart_min_temp` → Filtration Smart Min Temp (°C)  
- `sensor.vistapool_filtration_smart_max_temp` → Filtration Smart Max Temp (°C)  
- `binary_sensor.vistapool_filtration_status` → Filtration Running  

### 🧂 Salt Cell
- `binary_sensor.vistapool_salt_electrolysis_active` → Electrolysis Active  
- `sensor.vistapool_salt_level` → Salt Level (%)  
- `sensor.vistapool_salt_cell_runtime_total` → Total Runtime (h)  
- `sensor.vistapool_salt_cell_runtime_partial` → Partial Runtime (h)  

### 💡 Other Binary Sensors
- `binary_sensor.vistapool_light_status` → Pool Light Status (On/Off)  
- `binary_sensor.vistapool_uv_status` → UV Lamp Active  
- `binary_sensor.vistapool_ph_pump_active` → pH Pump Active  
- `binary_sensor.vistapool_chlorine_pump_active` → Chlorine Pump Active  

### 📶 Connectivity
- `sensor.vistapool_controller_firmware_version` → Controller Firmware Version  
- `sensor.vistapool_wifi_firmware_version` → WiFi Firmware Version  
- `sensor.vistapool_wifi_signal_strength` → WiFi Signal Strength (dBm)  
- `sensor.vistapool_wifi_serial` → WiFi Module Serial  

### ℹ️ Enriched Device Info
- Manufacturer: **Hayward**  
- Model: **VistaPool WiFi Module**  
- Firmware: `main.version`  
- Serial Number: `wifi`  

---

## 📦 Installation

1. Copy the folder `hayward_vistapool` into your Home Assistant `config/custom_components/` directory.  
   Final path should be:  

2. Restart Home Assistant.

3. In Home Assistant, go to **Settings → Devices & Services → Integrations → Add Integration**.  
Search for **Hayward VistaPool**.

---

## ⚙️ Configuration

During setup, you’ll need to provide:
- **Email** → your VistaPool account email  
- **Password** → your VistaPool account password  
- **Pool ID** → visible in the Firestore API document path, or in your VistaPool app data  

### Options
- **Scan Interval** → how often to poll VistaPool cloud for data.  
Default: `600` seconds (10 minutes).  
Dropdown options include: `10m`, `30m`, `1h`, `6h`, `12h`, `24h`.

- **Enable Debug** → enables verbose logging for troubleshooting.  

---

## 📝 Notes

- This integration is **unofficial** and not affiliated with Hayward.  
- It uses the Firebase + Firestore backend exposed by VistaPool / PoolWatch modules.  
- Supports writable setpoints for ORP, pH low, and pH high via Home Assistant number entities.  

---

💡 Developed with ❤️ by **Searise Developments Ltd.**  
Specialists in custom software development and avid contributors to the Home Assistant ecosystem.
