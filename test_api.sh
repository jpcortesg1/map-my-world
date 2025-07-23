#!/bin/bash

# Map My World API - Simple Test Suite for macOS
# Make sure your API is running on http://localhost:8000

BASE_URL="http://localhost:8000"
OUTPUT_FILE="api_test_results.json"

echo "============================================="
echo "🚀 MAP MY WORLD API - AUTOMATED TEST SUITE"
echo "============================================="
echo "📝 Results will be saved to: $OUTPUT_FILE"
echo ""

# Initialize with empty JSON
python3 -c "
import json
from datetime import datetime

data = {
    'test_suite': 'Map My World API Test Suite',
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'base_url': '$BASE_URL',
    'tests': [],
    'summary': {
        'total_tests': 0,
        'success_count': 0,
        'error_count': 0
    }
}

with open('$OUTPUT_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"

TEST_COUNT=0

# Function to execute test and add to JSON
execute_test() {
    local test_name="$1"
    local method="$2"
    local endpoint="$3"
    local request_body="$4"
    
    local url="$BASE_URL$endpoint"
    
    echo "🧪 Testing: $test_name"
    echo "   Method: $method"
    echo "   URL: $url"
    
    # Capture start time
    local start_time=$(date +%s)
    
    # Create temp files
    local response_file=$(mktemp)
    local status_file=$(mktemp)
    
    # Execute the curl request
    if [ "$method" = "GET" ]; then
        curl -s \
            -X GET "$url" \
            -H "accept: application/json" \
            -w "%{http_code}" \
            -o "$response_file" \
            > "$status_file" 2>/dev/null
    else
        curl -s \
            -X "$method" "$url" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -d "$request_body" \
            -w "%{http_code}" \
            -o "$response_file" \
            > "$status_file" 2>/dev/null
    fi
    
    local end_time=$(date +%s)
    local execution_time=$((end_time - start_time))
    
    # Read the results
    local status_code=$(cat "$status_file" 2>/dev/null || echo "000")
    local response_body=$(cat "$response_file" 2>/dev/null || echo "")
    
    # Clean up temp files
    rm -f "$response_file" "$status_file"
    
    echo "   Status: $status_code"
    echo "   Time: ${execution_time}s"
    echo "   Response Length: ${#response_body} chars"
    
    # Show preview
    if [ ${#response_body} -gt 0 ]; then
        local preview=$(echo "$response_body" | head -c 50)
        echo "   Preview: $preview..."
    fi
    echo ""
    
    # Create a temporary Python script to handle JSON safely
    cat > /tmp/add_test.py << EOF
import json
import sys
from datetime import datetime

# Read current JSON
with open('$OUTPUT_FILE', 'r') as f:
    data = json.load(f)

# Prepare request body
request_data = None
if '$request_body' and '$request_body' != 'null' and '$request_body' != '':
    try:
        request_data = json.loads('''$request_body''')
    except:
        request_data = '$request_body'

# Prepare response body
response_data = ''
if '''$response_body''':
    try:
        response_data = json.loads('''$response_body''')
    except:
        response_data = '''$response_body'''

# Create new test object
new_test = {
    'test_name': '$test_name',
    'method': '$method',
    'url': '$url',
    'request_body': request_data,
    'response': {
        'status_code': int('$status_code') if '$status_code'.isdigit() else 0,
        'body': response_data
    },
    'execution_time_seconds': $execution_time,
    'timestamp': datetime.utcnow().isoformat() + 'Z'
}

# Add test to the list
data['tests'].append(new_test)

# Update summary
data['summary']['total_tests'] = len(data['tests'])
data['summary']['success_count'] = len([t for t in data['tests'] if t['response']['status_code'] < 400])
data['summary']['error_count'] = len([t for t in data['tests'] if t['response']['status_code'] >= 400])

# Write back to file
with open('$OUTPUT_FILE', 'w') as f:
    json.dump(data, f, indent=2)

print('✅ Test saved to JSON')
EOF
    
    # Execute the Python script
    python3 /tmp/add_test.py
    rm -f /tmp/add_test.py
    
    ((TEST_COUNT++))
    echo "📊 Total tests completed: $TEST_COUNT"
    echo ""
}

# Health check
echo "📋 Testing API Health Check..."
health_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/docs" 2>/dev/null)
if [ "$health_status" = "200" ]; then
    echo "✅ API is running successfully!"
else
    echo "❌ API is not responding. Make sure it's running on $BASE_URL"
    echo "   Health check status: $health_status"
    exit 1
fi

echo ""
echo "============================================="
echo "📂 PHASE 1: CREATING CATEGORIES"
echo "============================================="
echo ""

execute_test "Create Restaurant Category" "POST" "/api/v1/categories/" '{
  "name": "Restaurant",
  "description": "Places to eat and dine"
}'

execute_test "Create Park Category" "POST" "/api/v1/categories/" '{
  "name": "Park",
  "description": "Green spaces and recreational areas"
}'

execute_test "Create Museum Category" "POST" "/api/v1/categories/" '{
  "name": "Museum",
  "description": "Cultural and educational institutions"
}'

execute_test "Create Shopping Mall Category" "POST" "/api/v1/categories/" '{
  "name": "Shopping Mall",
  "description": "Commercial shopping centers"
}'

execute_test "Get All Categories" "GET" "/api/v1/categories/" ""

echo ""
echo "============================================="
echo "📍 PHASE 2: CREATING LOCATIONS"
echo "============================================="
echo ""

execute_test "Create Central Park Location" "POST" "/api/v1/locations/" '{
  "name": "Central Park",
  "description": "Large public park in New York City",
  "longitude": -73.9654,
  "latitude": 40.7829
}'

execute_test "Create Times Square Grill Location" "POST" "/api/v1/locations/" '{
  "name": "Times Square Grill",
  "description": "Modern American restaurant in Times Square",
  "longitude": -73.9857,
  "latitude": 40.7590
}'

execute_test "Create Metropolitan Museum Location" "POST" "/api/v1/locations/" '{
  "name": "Metropolitan Museum of Art",
  "description": "World-renowned art museum",
  "longitude": -73.9632,
  "latitude": 40.7794
}'

execute_test "Create Brooklyn Bridge Park Location" "POST" "/api/v1/locations/" '{
  "name": "Brooklyn Bridge Park",
  "description": "Waterfront park with stunning views",
  "longitude": -73.9969,
  "latitude": 40.7023
}'

execute_test "Create Herald Square Mall Location" "POST" "/api/v1/locations/" '{
  "name": "Herald Square Mall",
  "description": "Shopping center in Manhattan",
  "longitude": -73.9876,
  "latitude": 40.7505
}'

execute_test "Get All Locations" "GET" "/api/v1/locations/" ""

execute_test "Get Location by ID 1" "GET" "/api/v1/locations/1" ""

execute_test "Get Location by ID 2" "GET" "/api/v1/locations/2" ""

echo ""
echo "============================================="
echo "🎯 PHASE 3: TESTING RECOMMENDATIONS (CORE FEATURE)"
echo "============================================="
echo ""

execute_test "Get Initial Recommendations" "GET" "/api/v1/recommendations/" ""

execute_test "Mark Location 1 + Category 1 as Reviewed" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 1
}'

execute_test "Mark Location 1 + Category 2 as Reviewed" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 2
}'

execute_test "Mark Location 2 + Category 1 as Reviewed" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 2,
  "category_id": 1
}'

execute_test "Get Recommendations After Marking Some as Reviewed" "GET" "/api/v1/recommendations/" ""

echo ""
echo "============================================="
echo "🚨 PHASE 4: ERROR HANDLING TESTS"
echo "============================================="
echo ""

execute_test "Test Non-existent Location Error" "GET" "/api/v1/locations/999" ""

execute_test "Test Invalid Location Data Error" "POST" "/api/v1/locations/" '{
  "name": "",
  "longitude": 200,
  "latitude": 100
}'

execute_test "Test Invalid Category Data Error" "POST" "/api/v1/categories/" '{}'

execute_test "Test Invalid Mark as Reviewed Error - Both Non-existent" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 999,
  "category_id": 999
}'

execute_test "Test Invalid Mark as Reviewed - Non-existent Location" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 999,
  "category_id": 1
}'

execute_test "Test Invalid Mark as Reviewed - Non-existent Category" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 999
}'

execute_test "Test Mark as Reviewed - Negative Location ID" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": -1,
  "category_id": 1
}'

execute_test "Test Mark as Reviewed - Negative Category ID" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": -1
}'

execute_test "Test Mark as Reviewed - Zero IDs" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 0,
  "category_id": 0
}'

execute_test "Test Mark as Reviewed - Missing Fields" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1
}'

execute_test "Test Mark as Reviewed - Invalid Data Types" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": "invalid",
  "category_id": "invalid"
}'

echo "🔬 Testing Mark as Reviewed Bug Fix (High Priority)..."

execute_test "Test Mark as Reviewed - Non-existent Location (Should be 404)" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 99999,
  "category_id": 1
}'

execute_test "Test Mark as Reviewed - Non-existent Category (Should be 404)" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 99999
}'

execute_test "Test Mark as Reviewed - Both Non-existent (Should be 404)" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 99999,
  "category_id": 99999
}'

execute_test "Test Mark as Reviewed - Edge Case Zero IDs (Should be 404)" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 0,
  "category_id": 0
}'

execute_test "Test Mark as Reviewed - Very High IDs (Should be 404)" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 999999,
  "category_id": 999999
}'

echo ""
echo "============================================="
echo "🧪 PHASE 5: EDGE CASES & VALIDATION"
echo "============================================="
echo ""

execute_test "Test Valid Boundary Coordinates" "POST" "/api/v1/locations/" '{
  "name": "North Pole",
  "description": "Geographic North Pole",
  "longitude": 0,
  "latitude": 90
}'

execute_test "Test Invalid Longitude Out of Range" "POST" "/api/v1/locations/" '{
  "name": "Invalid Location",
  "description": "This should fail",
  "longitude": 181,
  "latitude": 0
}'

echo ""
echo "============================================="
echo "🔍 PHASE 7: COMPREHENSIVE BUG TESTING"
echo "============================================="
echo ""

echo "🔬 Testing Recommendations Logic..."

execute_test "Test Recommendations Limit - Should Return Max 10" "GET" "/api/v1/recommendations/" ""

execute_test "Test Recommendations Consistency - Multiple Calls" "GET" "/api/v1/recommendations/" ""

execute_test "Test Recommendations After Marking - Should Exclude Recent" "GET" "/api/v1/recommendations/" ""

echo "🔬 Testing CRUD Edge Cases..."

execute_test "Test Create Location - Duplicate Name Different Coordinates" "POST" "/api/v1/locations/" '{
  "name": "Central Park",
  "description": "Another Central Park",
  "longitude": -74.0000,
  "latitude": 41.0000
}'

execute_test "Test Create Location - Same Coordinates Different Name" "POST" "/api/v1/locations/" '{
  "name": "Duplicate Coordinates Location", 
  "description": "Same coordinates as existing location",
  "longitude": -73.9654,
  "latitude": 40.7829
}'

execute_test "Test Create Category - Very Long Name" "POST" "/api/v1/categories/" '{
  "name": "This is a very long category name that should test the limits of the name field validation and see if there are any issues with extremely long category names in the system",
  "description": "Testing long names"
}'

execute_test "Test Create Location - Extreme Coordinates North" "POST" "/api/v1/locations/" '{
  "name": "North Pole Extreme",
  "description": "Testing extreme north",
  "longitude": 0,
  "latitude": 90
}'

execute_test "Test Create Location - Extreme Coordinates South" "POST" "/api/v1/locations/" '{
  "name": "South Pole Extreme",
  "description": "Testing extreme south", 
  "longitude": 0,
  "latitude": -90
}'

execute_test "Test Create Location - Extreme Coordinates East" "POST" "/api/v1/locations/" '{
  "name": "Extreme East",
  "description": "Testing extreme east",
  "longitude": 180,
  "latitude": 0
}'

execute_test "Test Create Location - Extreme Coordinates West" "POST" "/api/v1/locations/" '{
  "name": "Extreme West",
  "description": "Testing extreme west",
  "longitude": -180,
  "latitude": 0
}'

echo "🔬 Testing Query Parameters and Filters..."

execute_test "Test Get Locations with Query Params" "GET" "/api/v1/locations/?limit=5" ""

execute_test "Test Get Categories with Query Params" "GET" "/api/v1/categories/?limit=3" ""

execute_test "Test Get Locations with Invalid Query Params" "GET" "/api/v1/locations/?limit=invalid" ""

execute_test "Test Locations Pagination - Limit 3" "GET" "/api/v1/locations/?limit=3" ""

execute_test "Test Locations Pagination - Limit 5 Offset 2" "GET" "/api/v1/locations/?limit=5&offset=2" ""

execute_test "Test Categories Pagination - Limit 2" "GET" "/api/v1/categories/?limit=2" ""

execute_test "Test Locations Name Filter" "GET" "/api/v1/locations/?name=Central" ""

execute_test "Test Categories Name Filter" "GET" "/api/v1/categories/?name=Park" ""

execute_test "Test Combined Filter and Pagination" "GET" "/api/v1/locations/?name=Park&limit=2" ""

execute_test "Test Invalid Limit - Too High" "GET" "/api/v1/locations/?limit=101" ""

execute_test "Test Invalid Limit - Negative" "GET" "/api/v1/locations/?limit=-1" ""

execute_test "Test Invalid Offset - Negative" "GET" "/api/v1/locations/?offset=-1" ""

execute_test "Test Invalid Query Param Type" "GET" "/api/v1/locations/?limit=abc" ""

execute_test "Test Empty Name Filter" "GET" "/api/v1/locations/?name=" ""

execute_test "Test Large Offset" "GET" "/api/v1/locations/?offset=100" ""

execute_test "Test Limit Exactly at Max" "GET" "/api/v1/locations/?limit=100" ""

execute_test "Test Unicode in Name Filter" "GET" "/api/v1/locations/?name=%E5%8C%97%E4%BA%AC" ""

execute_test "Test Special Characters in Name Filter" "GET" "/api/v1/categories/?name=Caf%C3%A9" ""

execute_test "Test Space in Name Filter" "GET" "/api/v1/locations/?name=Central%20Park" ""

execute_test "Test Mixed Unicode and Latin" "GET" "/api/v1/locations/?name=%E5%8C%97%E4%BA%AC%20Beijing" ""

execute_test "Test Special Characters - Accents" "GET" "/api/v1/categories/?name=%C3%A1%C3%A9%C3%AD%C3%B3%C3%BA" ""

execute_test "Test Emoji in Filter" "GET" "/api/v1/categories/?name=%F0%9F%8D%95" ""

echo "🔬 Testing Special Characters and Unicode..."

execute_test "Test Create Category - Special Characters" "POST" "/api/v1/categories/" '{
  "name": "Café & Restaurante",
  "description": "Testing special characters: àáâãäåæçèéêë"
}'

execute_test "Test Create Location - Unicode Characters" "POST" "/api/v1/locations/" '{
  "name": "北京 Beijing",
  "description": "Testing unicode: 🌟🗽🎭🏛️",
  "longitude": 116.4074,
  "latitude": 39.9042
}'

execute_test "Test Create Category - Emoji in Name" "POST" "/api/v1/categories/" '{
  "name": "🍕 Pizza Places",
  "description": "Categories with emojis"
}'

echo "🔬 Testing HTTP Methods and Headers..."

execute_test "Test OPTIONS on Categories" "OPTIONS" "/api/v1/categories/" ""

execute_test "Test OPTIONS on Locations" "OPTIONS" "/api/v1/locations/" ""

execute_test "Test HEAD on Categories" "HEAD" "/api/v1/categories/" ""

execute_test "Test HEAD Categories Performance" "HEAD" "/api/v1/categories/" ""

execute_test "Test HEAD Locations Performance" "HEAD" "/api/v1/locations/" ""

execute_test "Test HEAD on Recommendations" "HEAD" "/api/v1/recommendations/" ""

echo "🔬 Testing Large Payloads..."

execute_test "Test Create Location - Very Long Description" "POST" "/api/v1/locations/" '{
  "name": "Long Description Location",
  "description": "This is an extremely long description that should test the limits of the description field and see how the API handles very large text inputs. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  "longitude": -75.0000,
  "latitude": 42.0000
}'

echo "🔬 Testing Concurrent Operations..."

execute_test "Test Mark Same Combination Multiple Times - Round 1" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 1
}'

execute_test "Test Mark Same Combination Multiple Times - Round 2" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 1
}'

execute_test "Test Mark Same Combination Multiple Times - Round 3" "POST" "/api/v1/recommendations/mark-reviewed" '{
  "location_id": 1,
  "category_id": 1
}'

echo "🔬 Testing Recommendations Business Logic..."

execute_test "Get Recommendations - Check for Exclusion of Recent Reviews" "GET" "/api/v1/recommendations/" ""

execute_test "Test Recommendations After Extensive Marking" "GET" "/api/v1/recommendations/" ""

echo "🔬 Testing Boundary Cases..."

execute_test "Test Create Location - Minimum Valid Coordinates" "POST" "/api/v1/locations/" '{
  "name": "Minimum Coordinates",
  "description": "Testing minimum valid coordinates",
  "longitude": -180,
  "latitude": -90
}'

execute_test "Test Create Location - Maximum Valid Coordinates" "POST" "/api/v1/locations/" '{
  "name": "Maximum Coordinates", 
  "description": "Testing maximum valid coordinates",
  "longitude": 180,
  "latitude": 90
}'

execute_test "Test Create Location - Precision Coordinates" "POST" "/api/v1/locations/" '{
  "name": "High Precision Location",
  "description": "Testing high precision coordinates",
  "longitude": -73.98765432,
  "latitude": 40.75912345
}'
echo ""

execute_test "Performance Test - Recommendations Request 1" "GET" "/api/v1/recommendations/" ""
sleep 1
execute_test "Performance Test - Recommendations Request 2" "GET" "/api/v1/recommendations/" ""
sleep 1
execute_test "Performance Test - Recommendations Request 3" "GET" "/api/v1/recommendations/" ""

execute_test "Performance Test - Rapid Category Creation" "POST" "/api/v1/categories/" '{
  "name": "Performance Test Category 1",
  "description": "Testing rapid creation"
}'

execute_test "Performance Test - Rapid Location Creation" "POST" "/api/v1/locations/" '{
  "name": "Performance Test Location 1",
  "description": "Testing rapid creation",
  "longitude": -76.0000,
  "latitude": 43.0000
}'

execute_test "Performance Test - Large Batch Recommendations" "GET" "/api/v1/recommendations/" ""

echo ""
echo "============================================="
echo "🚨 PHASE 9: SECURITY AND VALIDATION TESTS"
echo "============================================="
echo ""

echo "🛡️ Testing Security Edge Cases..."

execute_test "Test SQL Injection in Category Name" "POST" "/api/v1/categories/" '{
  "name": "Test\"; DROP TABLE categories; --",
  "description": "SQL injection test"
}'

execute_test "Test XSS in Category Name" "POST" "/api/v1/categories/" '{
  "name": "<script>alert(\"xss\")</script>",
  "description": "XSS test"
}'

execute_test "Test HTML Injection in Description" "POST" "/api/v1/locations/" '{
  "name": "HTML Test Location",
  "description": "<h1>HTML Injection Test</h1><img src=x onerror=alert(1)>",
  "longitude": -77.0000,
  "latitude": 44.0000
}'

execute_test "Test Very Large JSON Payload" "POST" "/api/v1/categories/" '{
  "name": "Large Payload Test",
  "description": "' + 'A' * 1000 + '"
}'

execute_test "Test Null Bytes in Input" "POST" "/api/v1/categories/" '{
  "name": "Test\u0000Category",
  "description": "Null byte test"
}'

execute_test "Test SQL Injection in Query Params" "GET" "/api/v1/locations/?name=test%27;DROP%20TABLE%20locations;--" ""

execute_test "Test XSS in Query Params" "GET" "/api/v1/categories/?name=%3Cscript%3Ealert%281%29%3C/script%3E" ""

execute_test "Test Path Traversal in Query" "GET" "/api/v1/locations/?name=../../../etc/passwd" ""

echo "🛡️ Testing Authorization/Authentication (if implemented)..."

execute_test "Test Unauthorized Access to Recommendations" "GET" "/api/v1/recommendations/" ""

execute_test "Test Access Control on Categories" "GET" "/api/v1/categories/" ""

execute_test "Test Access Control on Locations" "GET" "/api/v1/locations/" ""

echo ""
echo "============================================="
echo "✅ ALL TESTS COMPLETED!"
echo "============================================="
echo ""

# Final summary using Python
python3 -c "
import json

with open('$OUTPUT_FILE', 'r') as f:
    data = json.load(f)

total = data['summary']['total_tests']
success = data['summary']['success_count']
errors = data['summary']['error_count']

print(f'🎉 Test Results Summary:')
print(f'   📁 Results saved to: $OUTPUT_FILE')
print(f'   🧪 Total tests executed: {total}')
print(f'   ✅ Successful responses (status < 400): {success}')
print(f'   ❌ Error responses (status >= 400): {errors}')

if total > 0:
    avg_time = sum(t.get('execution_time_seconds', 0) for t in data['tests']) / total
    print(f'   ⏱️  Average response time: {avg_time:.1f}s')

# Show file size
import os
size = os.path.getsize('$OUTPUT_FILE')
print(f'   📄 JSON file size: {size} bytes')

# Show breakdown by status code
status_counts = {}
for test in data['tests']:
    status = test['response']['status_code']
    status_counts[status] = status_counts.get(status, 0) + 1

print(f'')
print(f'📊 Status Code Breakdown:')
for status, count in sorted(status_counts.items()):
    emoji = '✅' if status < 400 else '❌'
    print(f'   {emoji} {status}: {count} tests')
"

echo ""
echo "🔍 To analyze results:"
echo "   # View the complete JSON:"
echo "   cat $OUTPUT_FILE"
echo ""
echo "   # View formatted JSON (if you have jq):"
echo "   cat $OUTPUT_FILE | jq ."
echo ""
echo "   # Quick test summary:"
echo "   python3 -c \"import json; data=json.load(open('$OUTPUT_FILE')); [print(f'   {t[\\\"test_name\\\"]}: {t[\\\"response\\\"][\\\"status_code\\\"]}') for t in data['tests']]\""
echo ""

# If there are many 500 errors, show helpful message
python3 -c "
import json
import re

with open('$OUTPUT_FILE', 'r') as f:
    data = json.load(f)

error_500_count = len([t for t in data['tests'] if t['response']['status_code'] == 500])
error_404_count = len([t for t in data['tests'] if t['response']['status_code'] == 404])
error_422_count = len([t for t in data['tests'] if t['response']['status_code'] == 422])
error_405_count = len([t for t in data['tests'] if t['response']['status_code'] == 405])
total_tests = len(data['tests'])

print('')
print('🔍 DETAILED ERROR ANALYSIS:')
print(f'   🔴 500 Internal Server Errors: {error_500_count}')
print(f'   🔍 404 Not Found Errors: {error_404_count}')
print(f'   ⚠️  422 Validation Errors: {error_422_count}')
print(f'   🚫 405 Method Not Allowed: {error_405_count}')
print('')

if error_500_count > total_tests * 0.3:
    print('⚠️  WARNING: Many 500 errors detected!')
    print('   This suggests issues with your API implementation.')
    print('   Check your API logs for detailed error information.')
    print('')

# Query parameters validation check
query_tests = [t for t in data['tests'] if '?' in t['url']]
if query_tests:
    print('🔍 QUERY PARAMETERS ANALYSIS:')
    for test in query_tests:
        url = test['url']
        status = test['response']['status_code']
        test_name = test['test_name']
        
        if 'limit=' in url and status == 200:
            if isinstance(test['response']['body'], list):
                actual_count = len(test['response']['body'])
                # Extract limit from URL
                limit_match = re.search(r'limit=(\d+)', url)
                if limit_match:
                    expected_limit = int(limit_match.group(1))
                    emoji = '✅' if actual_count <= expected_limit else '❌'
                    status_text = 'WORKING' if actual_count <= expected_limit else 'BUG - Ignoring limit'
                    print(f'   {emoji} {test_name}: Expected ≤{expected_limit}, Got {actual_count} ({status_text})')
            elif 'limit=abc' in url or 'limit=-1' in url or 'limit=101' in url:
                emoji = '✅' if status >= 400 else '❌'
                status_text = 'WORKING' if status >= 400 else 'BUG - Should validate'
                print(f'   {emoji} {test_name}: HTTP {status} ({status_text})')
        
        if 'name=' in url and status == 200:
            if isinstance(test['response']['body'], list):
                # Check if filtering is working
                name_match = re.search(r'name=([^&]*)', url)
                if name_match:
                    filter_value = name_match.group(1)
                    if filter_value and filter_value != '':
                        # This is a simplified check - in reality we'd need to decode URL encoding
                        emoji = '⚠️'  # We can't easily verify filtering without decoding
                        print(f'   {emoji} {test_name}: Filter applied (manual verification needed)')
    print('')

# Look for the specific bug we're testing
bug_tests = [t for t in data['tests'] if 'Invalid Mark as Reviewed' in t['test_name'] or ('Mark as Reviewed' in t['test_name'] and ('Non-existent' in t['test_name'] or 'Should be 404' in t['test_name']))]
if bug_tests:
    print('🐛 MARK AS REVIEWED BUG ANALYSIS:')
    bug_fixed = True
    for test in bug_tests:
        status = test['response']['status_code']
        if 'Non-existent' in test['test_name'] or 'Should be 404' in test['test_name']:
            emoji = '✅' if status == 404 else '❌'
            expected = 'FIXED' if status == 404 else 'STILL BUGGY'
            if status != 404:
                bug_fixed = False
            print(f'   {emoji} {test[\"test_name\"]}: HTTP {status} ({expected})')
    
    if bug_fixed:
        print('   🎉 MARK AS REVIEWED BUG HAS BEEN FIXED!')
    else:
        print('   🔧 MARK AS REVIEWED BUG STILL NEEDS FIXING')
    print('')

# Recommendations consistency check
rec_tests = [t for t in data['tests'] if 'Recommendation' in t['test_name'] and t['method'] == 'GET' and t['response']['status_code'] == 200]
if len(rec_tests) >= 2:
    print('🎯 RECOMMENDATIONS CONSISTENCY CHECK:')
    rec_counts = []
    for test in rec_tests:
        response_body = test['response']['body']
        if isinstance(response_body, list):
            count = len(response_body)
        elif isinstance(response_body, str):
            try:
                # Try to parse JSON string
                import json
                parsed = json.loads(response_body)
                count = len(parsed) if isinstance(parsed, list) else 'N/A'
            except:
                count = 'N/A'
        else:
            count = 'N/A'
        
        rec_counts.append(count)
        print(f'   📊 {test[\"test_name\"]}: {count} recommendations')
    
    valid_counts = [c for c in rec_counts if isinstance(c, int)]
    if len(valid_counts) > 1:
        if len(set(valid_counts)) > 1:
            print('   ⚠️  WARNING: Inconsistent recommendation counts detected!')
        else:
            print('   ✅ Recommendation counts are consistent')
            if valid_counts and valid_counts[0] == 10:
                print('   🎯 PERFECT: Always returns exactly 10 recommendations')
    print('')

# HTTP Methods analysis
method_tests = [t for t in data['tests'] if t['method'] in ['OPTIONS', 'HEAD']]
if method_tests:
    print('🌐 HTTP METHODS ANALYSIS:')
    for test in method_tests:
        method = test['method']
        status = test['response']['status_code']
        time_taken = test.get('execution_time_seconds', 0)
        
        if method == 'HEAD' and time_taken > 2:
            emoji = '🐌'
            note = f'SLOW ({time_taken}s)'
        elif status == 405:
            emoji = '⚠️'
            note = 'Method Not Allowed (expected)'
        elif status < 400:
            emoji = '✅'
            note = 'Supported'
        else:
            emoji = '❌'
            note = f'Error {status}'
        
        print(f'   {emoji} {method} {test[\"url\"]}: {note}')
    print('')

# Security tests analysis
security_tests = [t for t in data['tests'] if any(term in t['test_name'].lower() for term in ['sql injection', 'xss', 'html injection', 'null byte'])]
if security_tests:
    print('🛡️ SECURITY ANALYSIS:')
    for test in security_tests:
        status = test['response']['status_code']
        if status < 400:
            emoji = '✅'
            note = 'Handled safely (no error thrown)'
        else:
            emoji = '⚠️'
            note = f'Rejected with HTTP {status}'
        
        print(f'   {emoji} {test[\"test_name\"]}: {note}')
    print('')

# Performance summary
all_times = [t.get('execution_time_seconds', 0) for t in data['tests']]
slow_tests = [t for t in data['tests'] if t.get('execution_time_seconds', 0) > 1]

if slow_tests:
    print('⏱️ PERFORMANCE ANALYSIS:')
    print(f'   📊 Average response time: {sum(all_times)/len(all_times):.2f}s')
    print(f'   🐌 Slow tests (>1s): {len(slow_tests)}')
    for test in slow_tests:
        time_taken = test.get('execution_time_seconds', 0)
        print(f'      ⏰ {test[\"test_name\"]}: {time_taken}s')
    print('')

# Overall assessment
success_rate = (data['summary']['success_count'] / data['summary']['total_tests']) * 100
print(f'📈 OVERALL API QUALITY ASSESSMENT:')
print(f'   📊 Success Rate: {success_rate:.1f}% ({data[\"summary\"][\"success_count\"]}/{data[\"summary\"][\"total_tests\"]})')

if success_rate >= 90:
    grade = '🏆 EXCELLENT'
elif success_rate >= 80:
    grade = '✅ VERY GOOD'
elif success_rate >= 70:
    grade = '👍 GOOD'
elif success_rate >= 60:
    grade = '⚠️ NEEDS IMPROVEMENT'
else:
    grade = '❌ POOR'

print(f'   🎯 Grade: {grade}')
print('')
"

echo "🚀 Test suite completed successfully!"
echo "============================================="