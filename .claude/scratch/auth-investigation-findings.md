# UCI API Authentication Investigation - Findings

**Date**: June 1, 2025  
**Branch**: feature/uci-auth

## Investigation Summary

We investigated the UCI calendar Excel download API to understand authentication requirements and enable automated downloads.

## Key Findings

### 1. HAR File Analysis Results

**Successful Request Details** (from user's browser):
- **URL**: `https://api.uci.ch/v1.2/ucibws/competitions/getreportxls`
- **Method**: POST
- **Status**: 200 OK
- **Response**: Excel file (103,857 bytes)
- **Content-Type**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**No Authentication Required** (from HAR analysis):
- No Authorization header
- No Bearer tokens
- No session cookies
- No API keys

### 2. Attempted Replication

**Request Configuration** (exact match to HAR):
```python
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd", 
    "accept-language": "en-GB,en;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.uci.org",
    "referer": "https://www.uci.org/",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site", 
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36..."
}

payload = {
    "IsGrouped": True,
    "Language": "En",
    "Query": {"discipline": "MTB", "year": "2025"},
    "ReportTitle": "MTB - 2025"
}
```

**Result**: 403 Forbidden
```json
{"message":"Forbidden"}
```

### 3. Analysis of Discrepancy

**Possible Protection Mechanisms**:

1. **Geographic Restrictions**:
   - HAR file shows CloudFront pop: `SFO53-P3` (San Francisco)
   - Our request routed to: `LHR3-P1` (London)
   - Different geographic routing might have different protection rules

2. **Rate Limiting / IP Restrictions**:
   - API might have per-IP rate limits
   - Automated requests from server IPs might be blocked
   - Browser vs script user-agent detection

3. **Session Context**:
   - Although no explicit session cookies in HAR, there might be implicit browser state
   - Previous page visits might set up required context
   - JavaScript-generated tokens not visible in HAR

4. **Cloudflare Protection**:
   - Response headers show Cloudflare is active
   - Might have bot detection / DDoS protection
   - Could require browser challenge completion

5. **API Changes**:
   - API might have changed protection since HAR capture
   - Temporary vs permanent access patterns

### 4. Alternative Approaches

**Option 1: Browser Automation**
- Use Selenium/Playwright to automate real browser
- Navigate to UCI site, trigger download through actual browser
- Handles any JavaScript/session requirements automatically

**Option 2: Session Context Replication**
- First visit UCI calendar page to establish session
- Then attempt API call with any cookies/context established
- Mimics full browser flow

**Option 3: Headless Browser API**
- Use headless Chrome to execute actual page JavaScript
- Intercept the download request and capture file
- Most robust but heavier solution

### 5. Current Working Solution

**Manual Download Workflow** (confirmed working):
1. User visits UCI calendar manually
2. Downloads Excel files 
3. Saves to `/data` directory
4. Automated system processes all available files
5. Weekly schedule means minimal manual intervention

## Recommendations

### Immediate: Hybrid Approach
1. **Keep manual workflow** as reliable fallback
2. **Implement browser automation** for attempt at full automation
3. **GitHub Actions enhancement** with fallback logic:
   ```
   try browser_automation_download()
   if failed:
       use existing_manual_files() 
   if no_files_found:
       notify_user_manual_download_needed()
   ```

### Future: Advanced Solutions
1. **Investigate session replication** with full page context
2. **Monitor for API changes** that might re-enable direct access
3. **Consider alternative data sources** if UCI provides other APIs

## Technical Implementation Notes

The authentication challenge is not actually about authentication - it's about sophisticated protection mechanisms that distinguish between browser and automated requests. The solution requires mimicking browser behavior more completely than just headers and payloads.

**Files Modified**:
- `scripts/download_uci_excel.py` - Updated with exact HAR headers (still blocked)
- `.claude/input/auth/` - Complete authentication flow capture and analysis

**Current Status**: 
- ✅ Authentication mechanism understood (none required)
- ✅ API endpoint and parameters confirmed  
- ❌ Direct API access blocked by protection layer
- ✅ Manual workflow functional and reliable
- 🔄 Browser automation approach identified for next iteration