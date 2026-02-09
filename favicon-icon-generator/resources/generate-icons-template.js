/**
 * Icon Generation Script Template
 * 
 * This script generates PNG icons from SVG for better browser compatibility.
 * Requires: npm install sharp
 */

const fs = require('fs');
const path = require('path');

console.log('📦 Icon Generation Script');
console.log('========================\n');

// Check if sharp is installed
try {
  const sharp = require('sharp');
  
  const publicDir = path.join(__dirname, '..', 'public');
  const iconSvgPath = path.join(publicDir, 'icon.svg');
  
  if (!fs.existsSync(iconSvgPath)) {
    console.error('❌ Error: icon.svg not found in public directory');
    process.exit(1);
  }

  // Define sizes to generate
  const sizes = [
    { name: 'apple-icon.png', size: 180 },
    { name: 'icon-192.png', size: 192 },
    { name: 'icon-512.png', size: 512 },
  ];

  console.log('🎨 Generating PNG icons from SVG...\n');

  Promise.all(
    sizes.map(async ({ name, size }) => {
      const outputPath = path.join(publicDir, name);
      
      await sharp(iconSvgPath)
        .resize(size, size)
        .png()
        .toFile(outputPath);
      
      console.log(`✅ Generated ${name} (${size}x${size})`);
    })
  ).then(() => {
    console.log('\n✨ All icons generated successfully!');
  }).catch(err => {
    console.error('❌ Error generating icons:', err);
    process.exit(1);
  });

} catch (err) {
  console.log('⚠️  Sharp library not installed.');
  console.log('\nTo generate PNG icons, install sharp:');
  console.log('  npm install --save-dev sharp');
  console.log('\nThen run:');
  console.log('  node scripts/generate-icons.js');
}
