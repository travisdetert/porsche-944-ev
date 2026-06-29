# Pi deployment — 944 head unit

Drops the app onto a Raspberry Pi: a **systemd service** runs the web server, **can0** comes up
on boot, and **Chromium kiosk** autostarts full-screen. Non-safety (ADR-0014) — the VCU/BMS run
independently. Hardware list: `../docs/headunit-bom.md`.

## Quick start
```bash
sudo apt-get install -y git
git clone <this-repo> ~/porsche-944-ev && cd ~/porsche-944-ev
bash deploy/install.sh
sudo reboot          # boots straight into the kiosk
```
Server: `http://localhost:8080` · check it: `systemctl status 944-headunit`.

## Bench mode (no car, no CAN HAT) — do this first
Edit `deploy/944-headunit.env`, comment out `CAN_IFACE`, then
`sudo systemctl restart 944-headunit`. The app runs on **mock data** — exactly what you see on
the laptop. Plug in any HDMI monitor + the Pi and you've got the head unit on the desk.

## Enabling the CAN HAT (MCP2515) for real telemetry
1. Add to **`/boot/firmware/config.txt`** (crystal value depends on your HAT — check 8/12/16 MHz):
   ```
   dtparam=spi=on
   dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25
   ```
2. `sudo reboot`, then verify: `ip -details link show can0`.
3. `can0.service` brings it up at **500000** bitrate (edit it to match your bus) — confirm the
   openinverter/Leaf bus rate before HV power-up.
4. Decode real frames: fill **`../app/can_map.json`** with the actual IDs/offsets, keep
   `CAN_IFACE=can0` in the env. `candump can0` helps you see live frames while mapping.

## Phone as a second screen + uplink
- **Pi as Wi-Fi AP** (phone joins → opens the same URL): simplest is NetworkManager —
  `sudo nmcli device wifi hotspot ssid 944EV password <pass>` (or RaspAP for a managed setup).
- **Internet uplink:** join your iPhone's Personal Hotspot as a client for live maps/weather, or
  add an LTE HAT later. (See the connectivity notes in the chat / ADR-0014.)

## Files
- `944-headunit.service` — runs `app/backend/server.py` (paths/user filled by install.sh)
- `can0.service` — `ip link set can0 up type can bitrate 500000`
- `944-headunit.env` — `CAN_IFACE`, `KIOSK_URL`
- `kiosk.sh` — waits for the server, launches Chromium kiosk, disables blanking/cursor
- `install.sh` — installs deps + services + kiosk autostart

## Notes / gotchas
- Kiosk needs the **desktop** image (it launches Chromium in the graphical session).
- On a clean power-off, the **UPS/ignition-shutdown HAT** (BOM item) prevents SD corruption.
- Pre-cache map tiles for offline use in the car.
