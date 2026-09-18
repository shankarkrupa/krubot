# Skill: Quick Dataset Filtering with Pagination

## Pattern for Large Datasets (10k+ records)

```bash
# 1. First check date range (verify if data spans target year)
termux-call-log -l 50
# If missing records, use pagination
termux-call-log -l 50 -o 50
```

## Python Template for Date/YEAR Filtering

```python
import json
from datetime import datetime

with open('data.json') as f:
    data = json.load(f)

mins = 0
for c in data:
    # Parse once, filter by year
    try:
        y = int(c['date'].split('-')[0])
        if str(y) != '2026': continue
        
        # Skip MISSED (duration=00:00 or type=MISSED)
        dur = c.get('duration', '')
        ct = c['type']
        if dur == '00:00' or ct.lower() == 'missed': continue
        
        # Parse as HH:MM (handles unusual formats like 58:04)
        h,m = int(dur.split(':')[0]), int(dur.split(':')[-1])
        mins += h*60 + m
                
    except: continue

print(f"{mins//60:,} hours")
```

## Key Rules

| DO | DON'T |
|---|---|
| Pagination (-o offset) if needed | Assume one query = all data |
| Parse date ONCE, compare string years | Re-parse after filtering |
| Skip MISSED/zero-duration | Count everything |
| Handle unusual durations (>24hrs) | Assume standard format |

## Quick Command Pattern
```
termux-call-log -l 100    → Check range
[if partial] termux-call-log -l 500 -o 500 → Get more data
python script.py          → Filter, sum minutes by year
```

