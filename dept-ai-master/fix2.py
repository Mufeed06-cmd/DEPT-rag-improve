with open('admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the second </script> tag (end of the grid/modal block at line ~743)
# and the next <script> tag after it (section management block)
# Everything between them is orphaned code - remove it

import re

# Strategy: find all </script> and <script> positions
closes = [m.start() for m in re.finditer(r'</script>', content)]
opens  = [m.start() for m in re.finditer(r'<script>', content)]

print(f"</script> positions: {closes}")
print(f"<script> positions: {opens}")

# The orphaned block is between closes[1] (after grid block) and opens[2] (section mgmt)
# closes[1] = end of grid/modal script block
# opens[2]  = start of section management script block
if len(closes) >= 3 and len(opens) >= 3:
    orphan_start = closes[1] + len('</script>')
    orphan_end   = opens[2]
    orphaned = content[orphan_start:orphan_end]
    non_blank = [l for l in orphaned.split('\n') if l.strip()]
    print(f"Orphaned block: {len(non_blank)} non-blank lines")
    print("First 3 lines:", non_blank[:3])
    
    # Remove the orphaned block
    clean = content[:orphan_start] + '\n\n' + content[orphan_end:]
    
    # Also fix the en-dash encoding issue in column headers
    # The ' – ' (en-dash) may have been double-encoded
    clean = clean.replace('\u2013', '-')  # replace en-dash with hyphen in JS strings
    # Fix column header display: use plain hyphen in JS, looks fine
    
    with open('admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(clean)
    
    print(f"Done. Original: {len(content)} chars, Clean: {len(clean)} chars")
else:
    print("Could not find expected script block structure")
    print(f"Found {len(closes)} closes and {len(opens)} opens")
