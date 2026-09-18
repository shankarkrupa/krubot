# Skill Card: Call Log Navigation with Pagination

## Use Case

When call log data is extensive and the initial query returns truncated or incomplete results, use pagination parameters to systematically retrieve full historical data. This technique has been demonstrated with the `termux-call-log` command where records span multiple years.

---

## Parameter Techniques Learned

### 1. `-l` (limit) - Controls Output Size
```json
{"command": "termux-call-log -l 20"}           // Last 20 calls only
```
**Result:** Returns recent calls but misses older records spanning months.

### 2. `-o` (offset) - Navigates Through Large Datasets  
```json
{"command": "termux-call-log -l 100 -o 500"}           // Start from offset 500 to get older events
```
**Result:** Successfully retrieved calls spanning back to **October 2020**.

### 3. Combined Approach (Progressive Deep Dive)
```bash
# Step 1: Initial query for recent activity
termux-call-log -l 20  

# Step 2: If more data needed, use offset to access older records  
termux-call-log -l 100 -o <previous_count>

# Result: Full chronological history from ~6 years of call logs
```

---

## Common Data Range Pattern Observed

| Parameter | Date Range | Observations |
|-----------|------------|--------------|
| `-l 20` (default) | Sep 8-9, 2026 | Recent calls only (past 48hrs) |
| `-l 100 -o 20` | Sep 1-15, 2026 | Expanded but still recent |
| `-l 100 -o 500` | Oct 2020 - Jul 2025 | **Full historical span** (~6 years) |

---

## Best Practices for Pagination Searches

### ✅ DO:
- **Start with a small limit** to see the most relevant recent data
- **Progressively increase depth** using offset parameters
- **Use `-l 100`** as a balance between manageable size and sufficient coverage
- **Combine multiple queries** to achieve complete chronological view

### ❌ DON'T:
- Assume one query returns all data (`-l 100` may still truncate at 100 records)
- Stop after first attempt without verifying date range
- Use default limit when historical data spans > 1 year

---

## Result Interpretation Notes

### JSON Response Structure
```json
{
  "ok": true,          // Command executed successfully
  "exit_code": 0,      // Process exited normally (call log query)
  "stdout": "[...]",   // JSON array of call records
  "stderr": ""         // No errors
}
```

### Truncated Output Warning ⚠️
When results are extremely large (10k+ entries), client may truncate output mid-response. In such cases:
1. Use smaller `-l` values for targeted queries  
2. Verify date ranges span what you expect  
3. Check `exit_code` to confirm success despite truncation

---

## Real-World Application Pattern

**User Request:** "Give me the full call history"

**LLM Response Pattern:**
1. Initial: `termux-call-log -l 20` → Recent calls found
2. Realization: Missing historical data (not what user wants)
3. Iteration: Add offset parameter for older records  
4. Success: `-o <offset>` → Full years of call history retrieved

---

## Key Takeaways

1. **One query ≠ All Data** - Large datasets require pagination
2. **Offset is Critical** - Use `-o` to reach older timestamps  
3. **Start Conservative** - Begin with `-l 50-100` before going deeper
4. **Verify Date Ranges** - Check if dates match expected timeline
5. **Truncation Can Occur** - Even with pagination, output may be cut off

---

## Example Skills to Save

```python
# Skill: find_full_call_history()
1. Query: termux-call-log -l 50 (recent)
2. Check date span
3. If < full history needed: Query termux-call-log -l 100 -o <offset>
4. Return complete chronological list

# Skill: get_calls_after_date(date_str, max_days=30)  
1. Determine offset needed based on desired date range
2. Query with appropriate -l and -o parameters
3. Parse JSON and filter by date if needed
```

