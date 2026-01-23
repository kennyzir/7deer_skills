/**
 * SEO Audit Script (Enhanced for Next.js)
 * Checks for comprehensive SEO issues in an HTML file.
 * 
 * Usage: node audit_rules.js <path_to_html_file>
 * 
 * Features:
 * - H1 tag check
 * - Meta description check  
 * - Canonical URL check
 * - Title length check
 * - OpenGraph tags check
 * - JSON-LD structured data check
 * - Internal links analysis
 * - Heading hierarchy check
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
    let score = 0;
    let maxScore = 0;

    // ============================================
    // 1. H1 Tag Check
    // ============================================
    maxScore += 10;
    const h1Matches = html.match(/<h1[^>]*>([^<]*)<\/h1>/gi);
    if (!h1Matches || h1Matches.length === 0) {
        results.push({ type: 'ERROR', category: 'Content', message: 'Missing H1 tag.' });
    } else if (h1Matches.length > 1) {
        results.push({ type: 'WARN', category: 'Content', message: `Multiple H1 tags found (${h1Matches.length}). Only one H1 is recommended.` });
        score += 5;
    } else {
        results.push({ type: 'OK', category: 'Content', message: 'Single H1 tag found.' });
        score += 10;
    }

    // ============================================
    // 2. Meta Description Check
    // ============================================
    maxScore += 10;
    const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i);
    if (!descMatch) {
        results.push({ type: 'ERROR', category: 'Meta', message: 'Missing <meta name="description">.' });
    } else {
        const descLength = descMatch[1].length;
        if (descLength < 100) {
            results.push({ type: 'WARN', category: 'Meta', message: `Description too short (${descLength} chars). Recommend 120-160.` });
            score += 5;
        } else if (descLength > 180) {
            results.push({ type: 'WARN', category: 'Meta', message: `Description too long (${descLength} chars). Recommend 120-160.` });
            score += 5;
        } else {
            results.push({ type: 'OK', category: 'Meta', message: `Description length OK (${descLength} chars).` });
            score += 10;
        }
    }

    // ============================================
    // 3. Canonical URL Check
    // ============================================
    maxScore += 10;
    const canonicalMatch = html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']*)["']/i);
    if (!canonicalMatch) {
        results.push({ type: 'WARN', category: 'Meta', message: 'Missing <link rel="canonical">.' });
    } else {
        results.push({ type: 'OK', category: 'Meta', message: `Canonical URL: ${canonicalMatch[1]}` });
        score += 10;
    }

    // ============================================
    // 4. Title Check
    // ============================================
    maxScore += 10;
    const titleMatch = html.match(/<title>([^<]*)<\/title>/i);
    if (!titleMatch) {
        results.push({ type: 'ERROR', category: 'Meta', message: 'Missing <title> tag.' });
    } else {
        const titleText = titleMatch[1].trim();
        const titleLength = titleText.length;
        if (titleLength < 30) {
            results.push({ type: 'WARN', category: 'Meta', message: `Title too short (${titleLength} chars): "${titleText}"` });
            score += 5;
        } else if (titleLength > 70) {
            results.push({ type: 'WARN', category: 'Meta', message: `Title too long (${titleLength} chars). May be truncated in SERPs.` });
            score += 7;
        } else {
            results.push({ type: 'OK', category: 'Meta', message: `Title length OK (${titleLength} chars).` });
            score += 10;
        }
    }

    // ============================================
    // 5. OpenGraph Tags Check
    // ============================================
    maxScore += 10;
    const ogTags = ['og:title', 'og:description', 'og:url', 'og:type'];
    let ogFound = 0;
    ogTags.forEach(tag => {
        const regex = new RegExp(`<meta\\s+property=["']${tag}["']`, 'i');
        if (regex.test(html)) ogFound++;
    });
    if (ogFound === 0) {
        results.push({ type: 'ERROR', category: 'Social', message: 'No OpenGraph tags found.' });
    } else if (ogFound < ogTags.length) {
        results.push({ type: 'WARN', category: 'Social', message: `OpenGraph incomplete (${ogFound}/${ogTags.length} tags). Missing some OG tags.` });
        score += Math.round(10 * ogFound / ogTags.length);
    } else {
        results.push({ type: 'OK', category: 'Social', message: `All ${ogTags.length} OpenGraph tags present.` });
        score += 10;
    }

    // ============================================
    // 6. Twitter Card Check
    // ============================================
    maxScore += 5;
    const twitterCard = html.match(/<meta\s+(name|property)=["']twitter:card["']/i);
    if (!twitterCard) {
        results.push({ type: 'WARN', category: 'Social', message: 'Missing Twitter Card meta tag.' });
    } else {
        results.push({ type: 'OK', category: 'Social', message: 'Twitter Card present.' });
        score += 5;
    }

    // ============================================
    // 7. JSON-LD Structured Data Check
    // ============================================
    maxScore += 15;
    const jsonLdMatch = html.match(/<script\s+type=["']application\/ld\+json["']>([^<]+)<\/script>/gi);
    if (!jsonLdMatch) {
        results.push({ type: 'WARN', category: 'Schema', message: 'No JSON-LD structured data found.' });
    } else {
        let validSchemas = 0;
        let schemaTypes = [];
        jsonLdMatch.forEach(script => {
            try {
                const jsonContent = script.match(/>([^<]+)</)[1];
                const data = JSON.parse(jsonContent);
                if (data['@type']) {
                    schemaTypes.push(data['@type']);
                    validSchemas++;
                }
            } catch (e) {
                results.push({ type: 'WARN', category: 'Schema', message: 'Invalid JSON-LD syntax detected.' });
            }
        });
        if (validSchemas > 0) {
            results.push({ type: 'OK', category: 'Schema', message: `JSON-LD found: ${schemaTypes.join(', ')}` });
            score += 15;
        }
    }

    // ============================================
    // 8. Internal Links Check
    // ============================================
    maxScore += 10;
    const internalLinks = html.match(/<a\s+[^>]*href=["']\/[^"']*["'][^>]*>/gi) || [];
    const uniqueInternalLinks = [...new Set(internalLinks.map(link => {
        const match = link.match(/href=["']([^"']*)["']/);
        return match ? match[1] : '';
    }))].filter(l => l && !l.startsWith('/#'));

    if (uniqueInternalLinks.length < 3) {
        results.push({ type: 'WARN', category: 'Links', message: `Only ${uniqueInternalLinks.length} internal links. Recommend 3-10.` });
        score += uniqueInternalLinks.length * 2;
    } else if (uniqueInternalLinks.length > 50) {
        results.push({ type: 'WARN', category: 'Links', message: `Too many internal links (${uniqueInternalLinks.length}). May dilute link equity.` });
        score += 7;
    } else {
        results.push({ type: 'OK', category: 'Links', message: `Good internal linking (${uniqueInternalLinks.length} unique links).` });
        score += 10;
    }

    // ============================================
    // 9. Heading Hierarchy Check
    // ============================================
    maxScore += 10;
    const headings = html.match(/<h[1-6][^>]*>/gi) || [];
    const headingLevels = headings.map(h => parseInt(h.match(/<h([1-6])/)[1]));
    let hierarchyOk = true;
    for (let i = 1; i < headingLevels.length; i++) {
        if (headingLevels[i] - headingLevels[i - 1] > 1) {
            hierarchyOk = false;
            break;
        }
    }
    if (!hierarchyOk) {
        results.push({ type: 'WARN', category: 'Content', message: 'Heading hierarchy skips levels (e.g., H1 -> H3).' });
        score += 5;
    } else {
        results.push({ type: 'OK', category: 'Content', message: 'Heading hierarchy is correct.' });
        score += 10;
    }

    // ============================================
    // 10. External Links Check
    // ============================================
    maxScore += 10;
    const externalLinks = html.match(/<a\s+[^>]*href=["']https?:\/\/[^"']*["'][^>]*>/gi) || [];
    const hasNofollow = externalLinks.filter(l => /rel=["'][^"']*noopener/.test(l)).length;
    if (externalLinks.length > 0) {
        const secureRatio = hasNofollow / externalLinks.length;
        if (secureRatio < 0.5) {
            results.push({ type: 'WARN', category: 'Links', message: `External links missing rel="noopener" (${hasNofollow}/${externalLinks.length}).` });
            score += 5;
        } else {
            results.push({ type: 'OK', category: 'Links', message: `External links properly secured (${externalLinks.length} links).` });
            score += 10;
        }
    } else {
        results.push({ type: 'OK', category: 'Links', message: 'No external links found.' });
        score += 10;
    }

    // ============================================
    // Output Results
    // ============================================
    const percentage = Math.round((score / maxScore) * 100);
    const grade = percentage >= 90 ? 'A' : percentage >= 80 ? 'B' : percentage >= 70 ? 'C' : percentage >= 60 ? 'D' : 'F';

    console.log(`\n${'═'.repeat(60)}`);
    console.log(`📋 SEO AUDIT REPORT: ${path.basename(filePath)}`);
    console.log(`${'═'.repeat(60)}`);
    console.log(`\n🏆 SCORE: ${score}/${maxScore} (${percentage}%) - Grade ${grade}\n`);

    // Group by category
    const categories = {};
    results.forEach(r => {
        if (!categories[r.category]) categories[r.category] = [];
        categories[r.category].push(r);
    });

    Object.keys(categories).forEach(cat => {
        console.log(`\n📂 ${cat}`);
        console.log(`${'─'.repeat(40)}`);
        categories[cat].forEach(r => {
            const icon = r.type === 'OK' ? '✅' : r.type === 'WARN' ? '⚠️' : '❌';
            console.log(`  ${icon} ${r.message}`);
        });
    });

    console.log(`\n${'═'.repeat(60)}\n`);

    return { score, maxScore, percentage, grade, results };
}

// Main
const filePath = process.argv[2];
if (!filePath) {
    console.log('Usage: node audit_rules.js <path_to_html_file>');
    console.log('\nExample: node audit_rules.js ./out/trello.html');
    process.exit(0);
}

auditHtml(filePath);
