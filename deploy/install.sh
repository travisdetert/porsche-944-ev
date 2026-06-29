#!/usr/bin/env bash
# One-shot installer for the 944 head unit on Raspberry Pi OS (Bookworm).
# Installs deps, the web-server service, can0 bring-up, and the Chromium kiosk autostart.
# Run from the repo:  bash deploy/install.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
USR="${SUDO_USER:-$USER}"
HOME_DIR="$(getent passwd "$USR" | cut -d: -f6)"
echo "Repo: $REPO"
echo "User: $USR  ($HOME_DIR)"

echo "==> Installing packages"
sudo apt-get update
sudo apt-get install -y python3 python3-can can-utils curl unclutter chromium-browser \
  || sudo apt-get install -y python3 python3-can can-utils curl unclutter chromium

render() { sed -e "s#__REPO__#$REPO#g" -e "s#__USER__#$USR#g" "$1"; }

echo "==> Installing systemd services"
render "$REPO/deploy/944-headunit.service" | sudo tee /etc/systemd/system/944-headunit.service >/dev/null
sudo cp "$REPO/deploy/can0.service" /etc/systemd/system/can0.service
sudo systemctl daemon-reload
sudo systemctl enable --now 944-headunit.service
# can0 only comes up if the MCP2515 overlay is in config.txt (see README); harmless otherwise
sudo systemctl enable can0.service || true
sudo systemctl start can0.service 2>/dev/null || echo "   (can0 not present yet — add the overlay + reboot; see deploy/README.md)"

echo "==> Installing kiosk autostart"
chmod +x "$REPO/deploy/kiosk.sh"
install -d "$HOME_DIR/.config/autostart"
cat > "$HOME_DIR/.config/autostart/944-kiosk.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=944 Head Unit Kiosk
Exec=$REPO/deploy/kiosk.sh
X-GNOME-Autostart-enabled=true
EOF
chown -R "$USR:$USR" "$HOME_DIR/.config/autostart"

echo "==> Done."
echo "   Server:  http://localhost:8080  (systemctl status 944-headunit)"
echo "   Reboot to launch the kiosk:  sudo reboot"
echo "   Bench/no-CAN: comment out CAN_IFACE in deploy/944-headunit.env, then restart the service."
