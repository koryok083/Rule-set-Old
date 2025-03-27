#!/bin/bash

# Pastikan folder rules ada
mkdir -p rules

# Rule-set Indonesia (Bank + E-Wallet + Layanan Lokal)
grep -E "bank|bca|bni|bri|mandiri|jenius|ovo|gopay|dana|shopeepay|tokopedia|bukalapak|shopee|grab|gojek|telkomsel|indosat|xlaxiata|smartfren" all_rules.yaml > rules/indo.yaml

# Rule-set Bank Indo
grep -E "bank|bca|bni|bri|mandiri|jenius" all_rules.yaml > rules/bank_indo.yaml

# Rule-set WhatsApp
grep -i "whatsapp" all_rules.yaml > rules/whatsapp.yaml

# Rule-set Sosial Media
grep -i "facebook|instagram|twitter|tiktok|telegram" all_rules.yaml > rules/sosial_media.yaml

# Rule-set Streaming
grep -i "netflix|youtube|disney|hbo|primevideo" all_rules.yaml > rules/streaming.yaml

# Rule-set Gaming
grep -i "steam|epicgames|playstation|xbox|riotgames" all_rules.yaml > rules/gaming.yaml

# Rule-set Iklan / Ads
grep -i "adservice|doubleclick|tracking|ads" all_rules.yaml > rules/ads.yaml

echo "Rule-set processing complete!"
