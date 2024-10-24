#!/bin/bash

# Check if a target is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <target-domain>"
  exit 1
fi

TARGET=$1
OUTPUT_FILE="${TARGET}_subdomains.txt"
TEMP_FILE="temp_subdomains.txt"

echo "Starting subdomain enumeration for $TARGET..."

# Run subfinder
echo "Running subfinder..."
/opt/recon/subfinder -d "$TARGET" -silent >> "$TEMP_FILE"

# Run assetfinder
echo "Running assetfinder..."
/opt/recon/assetfinder -subs-only "$TARGET" >> "$TEMP_FILE"

echo "$TARGET" | /opt/recon/waybackurls | /opt/recon/unfurl -u domains >> "$TEMP_FILE"

echo "runnning cero"
/opt/recon/cero-linux-amd64 "$TARGET" >> "$TEMP_FILE"
echo "cero ended"

echo "running ctfr"
python3 /opt/recon/ctfr/ctfr.py -d rivian.com -o ctfr.txt
cat ctfr.txt >> "$TEMP_FILE"
echo "ctfr stop"

sort -u "$TEMP_FILE" > "$OUTPUT_FILE"
rm "$TEMP_FILE"
rm ctfr.txt
# Clean up temporary files

echo "Subdomain enumeration completed. Results saved in $OUTPUT_FILE"

