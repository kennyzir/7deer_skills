/**
 * SEO Audit Script (Basic)
 * Checks for common SEO issues in an HTML file.
 * 
 * Usage: node audit_rules.js <path_to_html_file>
 */

const fs = require('fs');
const path = require('path');

function auditHtml(filePath) {
    if (!fs.existsSync(filePath)) {
        console.error(`Error: File not found at ${filePath}`);
        process.exit(1);
    }

    const html = fs.readFileSync(filePath, 'utf-8');
    const results = [];

    // 1. Check H1 tags
    const h1Matches = html.match(/<h1[^>]*>/gi);
    if (!h1Matches || h1Matches.length === 0) {
        results.push({ type: 'ERROR', message: 'Missing H1 tag.' });
    } else if (h1Matches.length > 1) {
        results.push({ type: 'WARN', message: `Multiple H1 tags found (${h1Matches.length}). Only one H1 is recommended.` });
    } else {
        results.push({ type: 'OK', message: 'H1 tag found.' });
    }

    // 2. Check Meta Description
    const descMatch = html.match(/<meta\s+name=["']description["'][^>]*>/i);
    if (!descMatch) {
        results.push({ type: 'ERROR', message: 'Missing <meta name="description">.' });
    } else {
        results.push({ type: 'OK', message: 'Meta description found.' });
    }

    // 3. Check Canonical URL
    const canonicalMatch = html.match(/<link\s+rel=["']canonical["'][^>]*>/i);
    if (!canonicalMatch) {
        results.push({ type: 'WARN', message: 'Missing <link rel="canonical">. Canonical URL is recommended.' });
    } else {
        results.push({ type: 'OK', message: 'Canonical URL found.' });
    }

    // 4. Check Title Length
    const titleMatch = html.match(/<title>([^<]*)<\/title>/i);
    if (!titleMatch) {
        results.push({ type: 'ERROR', message: 'Missing <title> tag.' });
    } else {
        const titleLength = titleMatch[1].trim().length;
        if (titleLength < 30) {
            results.push({ type: 'WARN', message: `Title is too short (${titleLength} chars). Recommend 50-60.` });
        } else if (titleLength > 70) {
            results.push({ type: 'WARN', message: `Title is too long (${titleLength} chars). Recommend 50-60.` });
        } else {
            results.push({ type: 'OK', message: `Title length OK (${titleLength} chars).` });
        }
    }

    // --- Output Results ---
    console.log(`\n📋 SEO Audit Report: ${path.basename(filePath)}\n${'='.repeat(50)}`);
    results.forEach(r => {
        const icon = r.type === 'OK' ? '✅' : r.type === 'WARN' ? '⚠️' : '❌';
        console.log(`  ${icon} [${r.type}] ${r.message}`);
    });
    console.log('');
}

// Main
const filePath = process.argv[2];
if (!filePath) {
    console.log('Usage: node audit_rules.js <path_to_html_file>');
    process.exit(0);
}
auditHtml(filePath);
