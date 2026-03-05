import os, re, urllib.parse

public = "/home/node/.openclaw/workspace/jlptpath/public"
broken = []
total = 0

for root, dirs, files in os.walk(public):
    for f in files:
        if not f.endswith(".html"):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, public)
        with open(path) as fh:
            html = fh.read()
        
        for m in re.finditer(r'href=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]*))', html):
            link = m.group(1) or m.group(2) or m.group(3) or ""
            if not link or link.startswith("http") or link.startswith("#") or link.startswith("mailto:") or link.startswith("javascript:") or link.startswith("data:"):
                continue
            total += 1
            clean = link.split("#")[0].split("?")[0]
            if not clean or clean == "/":
                continue
            # URL-decode the path
            decoded = urllib.parse.unquote(clean)
            target = os.path.join(public, decoded.lstrip("/"))
            if not os.path.exists(target) and not os.path.exists(target + "/index.html") and not os.path.exists(target.rstrip("/") + "/index.html"):
                broken.append(f"{rel} → {link}")

print(f"Total internal links checked: {total}")
print(f"Broken internal links: {len(broken)}")
unique = sorted(set(broken))
for b in unique[:80]:
    print(f"  {b}")
if len(unique) > 80:
    print(f"  ... and {len(unique)-80} more")
