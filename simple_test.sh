#!/bin/bash

echo "=== SIMPLE API TEST ==="

# Test 1: Simple GET request
echo "Test 1: GET /api/v1/locations/"
response=$(curl -s -X GET "http://localhost:8000/api/v1/locations/" -H "accept: application/json" -w "%{http_code}")
echo "Response: $response"
echo ""

# Test 2: GET with status code
echo "Test 2: GET /api/v1/locations/ with status"
status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/api/v1/locations/")
echo "Status: $status"
echo ""

# Test 3: Test the exact curl command from the script
echo "Test 3: Exact curl command from script"
response_file=$(mktemp)
status_file=$(mktemp)

curl -s \
    -X GET "http://localhost:8000/api/v1/locations/" \
    -H "accept: application/json" \
    -w "%{http_code}" \
    -o "$response_file" \
    > "$status_file" 2>/dev/null

status_code=$(cat "$status_file" 2>/dev/null || echo "000")
response_body=$(cat "$response_file" 2>/dev/null || echo "")

echo "Status code: $status_code"
echo "Response body length: ${#response_body}"
echo "Response body preview: ${response_body:0:100}"

rm -f "$response_file" "$status_file"
echo "=== TEST COMPLETED ===" 