# Subdomain Enumaration Using Web Archive

function wayback() {
  curl -sk "http://web.archive.org/cdx/search/cdx?url=*.$1&output=txt&fl=original&collapse=urlkey&page=" | awk -F/ '{gsub(/:.*/, "", $3); print $3}' | sort -u
}