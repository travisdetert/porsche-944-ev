#!/usr/bin/env bash
# Wait for the head-unit server, then launch Chromium full-screen kiosk.
# Started by the desktop autostart entry that install.sh drops in.
set -u
URL="${KIOSK_URL:-http://localhost:8080}"

# stop the screen from blanking (X session)
xset s off -dpms 2>/dev/null || true
xset s noblank 2>/dev/null || true
command -v unclutter >/dev/null && unclutter -idle 0.5 -root &   # hide the cursor

# wait until the server answers
until curl -sf "$URL" >/dev/null 2>&1; do sleep 1; done

CHROME="$(command -v chromium-browser || command -v chromium || echo chromium-browser)"
exec "$CHROME" --kiosk --noerrdialogs --disable-infobars --incognito \
  --check-for-update-interval=31536000 --disable-pinch \
  --overscroll-history-navigation=0 --autoplay-policy=no-user-gesture-required \
  "$URL"
