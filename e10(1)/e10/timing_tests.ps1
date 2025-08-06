# Timing script for reddit_averages performance comparison
Write-Host "=== Reddit Averages Performance Timing ==="
Write-Host ""

# Test 1: reddit-0 baseline (Spark startup time)
Write-Host "1. Testing reddit-0 (baseline - Spark startup time)..."
$baseline = (Measure-Command { 
        spark-submit --master="local[1]" reddit_averages.py reddit-0 timing-baseline 
    }).TotalSeconds
Write-Host "   Reddit-0 baseline: $baseline seconds"
Write-Host ""

# Test 2: reddit-1 with no schema, no cache
Write-Host "2. Testing reddit-1 with NO SCHEMA, NO CACHE..."
$time_no_schema_no_cache = (Measure-Command { 
        spark-submit --master="local[1]" reddit_averages_no_schema_no_cache.py reddit-1 timing-no-schema-no-cache 
    }).TotalSeconds
Write-Host "   No schema, no cache: $time_no_schema_no_cache seconds"
Write-Host ""

# Test 3: reddit-1 with schema, no cache
Write-Host "3. Testing reddit-1 with SCHEMA, NO CACHE..."
$time_schema_no_cache = (Measure-Command { 
        spark-submit --master="local[1]" reddit_averages_schema_no_cache.py reddit-1 timing-schema-no-cache 
    }).TotalSeconds
Write-Host "   Schema, no cache: $time_schema_no_cache seconds"
Write-Host ""

# Test 4: reddit-1 with schema and cache (optimized version)
Write-Host "4. Testing reddit-1 with SCHEMA AND CACHE (optimized)..."
$time_schema_cache = (Measure-Command { 
        spark-submit --master="local[1]" reddit_averages.py reddit-1 timing-schema-cache 
    }).TotalSeconds
Write-Host "   Schema and cache: $time_schema_cache seconds"
Write-Host ""

# Summary
Write-Host "=== TIMING RESULTS SUMMARY ==="
Write-Host "1. Reddit-0 (baseline):           $baseline seconds"
Write-Host "2. No schema, no cache:            $time_no_schema_no_cache seconds"
Write-Host "3. Schema, no cache:               $time_schema_no_cache seconds"
Write-Host "4. Schema and cache (optimized):   $time_schema_cache seconds"
Write-Host ""

# Calculate improvements
$improvement_schema = $time_no_schema_no_cache - $time_schema_no_cache
$improvement_cache = $time_schema_no_cache - $time_schema_cache
$total_improvement = $time_no_schema_no_cache - $time_schema_cache

Write-Host "=== PERFORMANCE IMPROVEMENTS ==="
Write-Host "Schema improvement:     $improvement_schema seconds"
Write-Host "Cache improvement:      $improvement_cache seconds"
Write-Host "Total improvement:      $total_improvement seconds"
