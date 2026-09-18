# Skill: Dataset Analysis with Pagination and Date Filtering

## Use Case

When users request data analysis over large historical datasets (like call logs spanning multiple years):
1. First check if default query captures full timeline
2. Use pagination (-o offset) to retrieve complete data  
3. Apply proper date/time parsing for accurate filtering
4. Handle edge cases like unusual duration formats

---

## Parameter Techniques Learned

### 1. Pagination Strategy for Large Datasets
```json
// Step 1: Initial query (recent data only)
termux-call-log -l 50

// Step 2: Add offset to access historical records  
termux-call-log -l 500 -o 500
```

### 2. Date Format Detection & Handling
When dates appear in format like "YYYY-MM-DD HH:MM:SS":
- **Parse correctly**: `datetime.strptime(date, '%Y-%m-%d %H:%M:%S')`
- **Handle edge cases**: Some records may have different formats (e.g., '27:34' instead of proper timestamps)
- **Filter by year**: Extract YYYY-MM-DD properly before comparing

### 3. Call Type Filtering  
Only count active calls, skip MISSED/zero-duration entries:
```python
if call['type'].lower() == 'missed': continue
if duration == '00:00': continue
```

### 4. Duration Parsing Edge Cases
Phone logs may have unusual durations:
- Standard HH:MM format (e.g., "58:04" > 24 hours possible)
- Some edge cases like '27:34' need different parsing
- Convert to minutes: `hours * 60 + minutes`

---

## Best Practices for Pagination Analysis

### ✅ DO:
- **Start with small limit** to verify date range coverage
- **Progressively use offset** parameters (-o) for complete data
- **Parse dates BEFORE applying filters** (don't parse year, then re-parse)
- **Check raw duration format** before assuming HH:MM structure
- **Handle malformed records gracefully** with try/except blocks

### ❌ DON'T:
- Assume single query returns all data (-l 100 may still truncate)
- Stop pagination without verifying date range matches expectation
- Use default limit when historical data spans > 6 years  
- Skip year validation on parsing errors (date strings vary!)

---

## Result Interpretation Patterns

### JSON Response Structure
```json
{
  "ok": true,        // Command executed successfully
  "exit_code": 0,    // Process exited normally
  "stdout": "[...]", // Array of record objects
  "stderr": ""       // Empty if no errors
}
```

### Date Validation Checklist
- `[YYYY-MM-DD HH:MM:SS]` - Standard format (parse with datetime)
- `[DD:HH:MM]` or malformed - May need custom parsing
- **Year extraction**: `year_str = date.split('-')[0]`
- **Filter safely**: `if str(year) == '2026': process()`

---

## Python Analysis Pattern Template

```python
import json
from datetime import datetime

with open('call_data.json') as f:
    data = json.load(f)

total_minutes = 0
records_count = 0

for call in data:
    try:
        # Step 1: Parse date safely
        year_str = call['date'].split('-')[0]
        
        # Step 2: Check year before processing
        parsed_year = int(year_str.replace('.', '').replace(' ', ''))
        if str(parsed_year) != '2026': continue
        
        # Step 3: Parse duration properly  
        dur_str = call.get('duration', '')
        ct_lower = call['type']
        
        # Skip MISSED calls
        if ct_lower.lower() == 'missed' or dur_str == '00:00':
            continue
        
        # Parse as HH:MM (includes values > 24hours)
        try:
            h, m = int(dur_str.split(':')[0]), int(dur_str.split(':')[-1])
            total_minutes += h * 60 + m
            records_count += 1
        except:
            continue
            
    except Exception as e:
        # Skip malformed records
        continue

print(f"Total: {total_minutes:,} minutes ({total_minutes // 60:,} hours)")
```

---

## Real-World Application Pattern

**User Request**: "Calculate total call minutes spanning year X"

**Recommended LLM Response Pattern:**
1. Query: `termux-call-log -l 50` → Verify date range
2. If partial: Add offset, e.g., `-o 50` for more old records
3. Extract year from dates in returned data
4. Use Python to sum only matching records
5. Report clearly: "X minutes across Y records"

---

## Key Takeaways

1. **Pagination is Critical** - One query rarely returns complete historical datasets
2. **Parse BEFORE Process** - Don't parse date, then re-parse; do it once correctly  
3. **Year Validation** - Compare year strings properly before processing
4. **Duration Edge Cases** - Phone logs may have unusual formats (hours > 24)
5. **Graceful Degradation** - Skip malformed records instead of crashing

---

## Example Skills to Save

```python
# Skill: find_full_call_history()
def get_2026_minutes():
    # Query multiple times with pagination offsets
    all_data = []
    for offset in range(0, 5000, 500):
        query = f"termux-call-log -l 100 -o {offset}"
        result = execute(query)
        all_data.extend(result)
    
    # Parse once using Python datetime module, filter by year
    minutes_2026 = sum_hours_minutes(data_from_year="2026")
    return total_minutes

# Skill: parse_malformed_timestamps()  
def safe_parse_dates(records):
    """Handle both YYYY-MM-DD HH:MM:SS and edge cases"""
    parsed = []
    for rec in records:
        # Try standard format first
        try: 
            dt = datetime.strptime(rec['date'], '%Y-%m-%d %H:%M:%S')
            year = str(dt.year)
            if year == '2026': parsed.append({'year': '2026', 'data': rec})
            continue
        except ValueError:
            pass
        
    return parsed  # Fallback handling...
```

