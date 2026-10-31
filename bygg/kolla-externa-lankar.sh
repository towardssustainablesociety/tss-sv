#!/bin/bash
# TSS: provar alla externa länkar på webbplatserna TSS-sv och TSS-en.
#
# Kör i Terminal på en dator med nätåtkomst, till exempel:
#   bash ~/"Library/Mobile Documents/com~apple~CloudDocs/TSS-förvaltning/kolla-externa-lankar.sh"
# eller direkt från GitHub:
#   curl -s https://raw.githubusercontent.com/towardssustainablesociety/tss-sv/main/bygg/kolla-externa-lankar.sh | bash
#
# Skriptet hämtar sidorna via webbplatsernas sitemap.xml, plockar ut de externa
# länkarna och provar var och en. Det skriver bara ut länkar som inte svarar med
# 200 (OK), och sidorna där de står.
#
# Så läses svaren:
#   403  nästan alltid en robotspärr (doi.org, science.org, oecd.org m.fl.); sidan
#        fungerar i webbläsaren och räknas inte som fel.
#   000  anslutningen gick inte att öppna; kontrollera länken i Safari.
#   404  och liknande: riktiga fel, som ska rättas.
#
# För att prova en webbplats som är byggd lokalt: ange mappen som argument,
#   bash kolla-externa-lankar.sh _site

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/605.1.15"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# 1. Hämta alla sidor till en tillfällig mapp (eller använd en lokal mapp).
if [ -n "$1" ] && [ -d "$1" ]; then
  find "$1" -name index.html | while read -r f; do
    sida="${f#$1}"; sida="${sida%index.html}"
    printf '%s\t%s\n' "lokalt$sida" "$f"
  done > "$TMP/sidor.tsv"
else
  echo "Hämtar sidorna på sv och en …"
  n=0
  for webb in https://sv.towardssustainablesociety.org https://en.towardssustainablesociety.org; do
    curl -s -A "$UA" --max-time 30 "$webb/sitemap.xml" \
      | grep -oE '<loc>[^<]+</loc>' | sed -e 's/<loc>//' -e 's/<\/loc>//' \
      | while read -r adress; do
          n=$((n+1)); fil="$TMP/sida$RANDOM$RANDOM.html"
          curl -s -A "$UA" --max-time 30 "$adress" -o "$fil"
          printf '%s\t%s\n' "$adress" "$fil"
        done
  done > "$TMP/sidor.tsv"
fi
antal_sidor=$(wc -l < "$TMP/sidor.tsv" | tr -d ' ')
if [ "$antal_sidor" = "0" ]; then
  echo "Hittade inga sidor. Har datorn kontakt med nätet?"; exit 1
fi

# 2. Plocka ut de externa länkarna, med sidan där varje länk står.
while IFS=$'\t' read -r adress fil; do
  grep -oE 'href="https?://[^"]+"' "$fil" \
    | sed -e 's/^href="//' -e 's/"$//' -e 's/&amp;/\&/g' \
    | grep -v 'towardssustainablesociety' \
    | grep -v 'creativecommons.org/licenses' \
    | grep -v '^https://github.com/towardssustainablesociety' \
    | while read -r u; do printf '%s\t%s\n' "$u" "$adress"; done
done < "$TMP/sidor.tsv" | sort -u > "$TMP/lankar.tsv"
cut -f1 "$TMP/lankar.tsv" | sort -u > "$TMP/unika.txt"
antal=$(wc -l < "$TMP/unika.txt" | tr -d ' ')
echo "Provar $antal externa länkar på $antal_sidor sidor …"

# 3. Prova länkarna.
fel=0; robot=0
while read -r u; do
  c=$(curl -s -o /dev/null -L --max-time 25 -A "$UA" -w "%{http_code}" "$u")
  if [ "$c" != "200" ]; then
    if [ "$c" = "403" ]; then robot=$((robot+1)); else fel=$((fel+1)); fi
    echo "$c  $u"
    awk -F'\t' -v u="$u" '$1==u {print "     på: " $2}' "$TMP/lankar.tsv" | head -4
  fi
done < "$TMP/unika.txt"
echo "Klart: $antal länkar. $robot gav 403 (robotspärr, oftast inget fel). $fel andra svar att kontrollera."
