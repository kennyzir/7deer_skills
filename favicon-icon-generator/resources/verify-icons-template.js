/**
 * Icon Verification Script Template
 * 
 * This script verifies that all required icon files exist and are properly configured.
 * Customize the file paths and requirements for your project.
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Icon Verification Script');
console.log('===========================\n');

// Configure your project paths
const publicDir = path.join(__dirname, '..', 'public');
const srcAppDir = path.join(__dirname, '..', 'src', 'app');

// Define required files
const requiredFiles = [
  { path: path.join(publicDir, 'icon.svg'), name: 'icon.svg', critical: true },
  { path: path.join(publicDir, 'favicon.svg'), name: 'favicon.svg', critical: true },
  { path: path.join(srcAppDir, 'apple-icon.png'), name: 'apple-icon.png', critical: true },
  { path: path.join(publicDir, 'manifest.json'), name: 'manifest.json', critical: true },
];

// Define optional files
const optionalFiles = [
  { path: path.join(publicDir, 'icon-192.png'), name: 'icon-192.png' },
  { path: path.join(publicDir, 'icon-512.png'), name: 'icon-512.png' },
];

let hasErrors = false;
let hasWarnings = false;

// Check required files
console.log('📋 Checking required files:\n');
requiredFiles.forEach(({ path: filePath, name, critical }) => {
  if (fs.existsSync(filePath)) {
    const stats = fs.statSync(filePath);
    const size = (stats.size / 1024).toFixed(2);
    console.log(`✅ ${name} (${size} KB)`);
  } else {
    console.log(`❌ ${name} - MISSING`);
    if (critical) hasErrors = true;
  }
});

// Check optional files
console.log('\n📋 Checking optional files:\n');
optionalFiles.forEach(({ path: filePath, name }) => {
  if (fs.existsSync(filePath)) {
    const stats = fs.statSync(filePath);
    const size = (stats.size / 1024).toFixed(2);
    console.log(`✅ ${name} (${size} KB)`);
  } else {
    console.log(`⚠️  ${name} - Not found (optional)`);
    hasWarnings = true;
  }
});

// Check manifest.json content
console.log('\n📋 Checking manifest.json configuration:\n');
const manifestPath = path.join(publicDir, 'manifest.json');
if (fs.existsSync(manifestPath)) {
  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    
    if (manifest.icons && manifest.icons.length > 0) {
      console.log(`✅ Found ${manifest.icons.length} icon(s) in manifest`);
      manifest.icons.forEach(icon => {
        console.log(`   - ${icon.src} (${icon.sizes || 'any'})`);
      });
    } else {
      console.log('❌ No icons found in manifest.json');
      hasErrors = true;
    }
  } catch (err) {
    console.log('❌ Error parsing manifest.json:', err.message);
    hasErrors = true;
  }
}

// Summary
console.log('\n' + '='.repeat(50));
if (hasErrors) {
  console.log('❌ VERIFICATION FAILED - Critical issues found');
  process.exit(1);
} else if (hasWarnings) {
  console.log('⚠️  VERIFICATION PASSED WITH WARNINGS');
  process.exit(0);
} else {
  console.log('✅ VERIFICATION PASSED - All icons configured correctly!');
  process.exit(0);
}
