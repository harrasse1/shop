/**
 * Generates beautiful SVG product placeholders for products without real photos.
 * Each SVG mimics the actual Forever Living product packaging style.
 */
const fs = require('fs');
const path = require('path');

// Product definitions matching products.js
// Each has: id, type (bottle/tube/box/jar/spray/perfume), color, label, accent
const PRODUCTS_CONFIG = [
  // Drinks
  { id: 'forever-freedom', type: 'bottle', color: '#2a5d8f', accent: '#f4a300', label: 'FREEDOM', sublabel: 'Aloe + Joint Support' },
  { id: 'pomesteen-power', type: 'bottle', color: '#8b1a3a', accent: '#d4af37', label: 'POMESTEEN', sublabel: 'POWER' },

  // Nutrition
  { id: 'forever-arctic-sea', type: 'bottle-cap', color: '#0e6b8a', accent: '#fff', label: 'ARCTIC SEA', sublabel: 'Omega-3' },
  { id: 'forever-daily', type: 'bottle-cap', color: '#2e7d32', accent: '#fff', label: 'FOREVER DAILY', sublabel: 'Multi-Vitamin' },
  { id: 'forever-calcium', type: 'bottle-cap', color: '#37474f', accent: '#fff', label: 'CALCIUM', sublabel: 'Bone Health' },

  // Bee
  { id: 'forever-bee-honey', type: 'jar', color: '#d4a017', accent: '#a8742e', label: 'BEE HONEY', sublabel: '100% Pure' },

  // Sonya Skincare
  { id: 'sonya-aloe-purifying-cleanser', type: 'tube-pump', color: '#e8b4b8', accent: '#fff', label: 'SONYA', sublabel: 'Cleanser' },
  { id: 'sonya-refreshing-toner', type: 'spray', color: '#a8d5ba', accent: '#fff', label: 'SONYA', sublabel: 'Toner' },
  { id: 'sonya-soothing-gel', type: 'tube', color: '#7eb09b', accent: '#fff', label: 'SONYA', sublabel: 'Soothing Gel' },
  { id: 'sonya-aloe-balancing-cream', type: 'jar', color: '#f0e0d6', accent: '#a87c1f', label: 'SONYA', sublabel: 'Balancing Cream' },

  // Skincare
  { id: 'forever-aloe-scrub', type: 'jar', color: '#c8a882', accent: '#5d4037', label: 'ALOE SCRUB', sublabel: 'Exfoliating' },
  { id: 'forever-aloe-bio-cellulose-mask', type: 'box', color: '#b8d8c8', accent: '#1a6b4e', label: 'BIO-CELLULOSE', sublabel: 'Mask' },
  { id: 'forever-marine-mask', type: 'jar', color: '#5d8aa8', accent: '#fff', label: 'MARINE', sublabel: 'Mask' },
  { id: 'r3-factor', type: 'tube', color: '#d4af37', accent: '#0b3d2e', label: 'R3 FACTOR', sublabel: 'Skin Defense' },
  { id: 'aloe-fleur-de-jouvence', type: 'box', color: '#c89a3a', accent: '#0b3d2e', label: 'FLEUR DE', sublabel: 'JOUVENCE' },

  // Weight
  { id: 'forever-fiber', type: 'box', color: '#558b2f', accent: '#fff', label: 'FOREVER', sublabel: 'FIBER' },
  { id: 'garcinia-plus', type: 'bottle-cap', color: '#8e24aa', accent: '#fff', label: 'GARCINIA', sublabel: 'PLUS' },
  { id: 'vital5', type: 'box', color: '#d4af37', accent: '#0b3d2e', label: 'VITAL 5', sublabel: 'Daily Pack' },

  // Personal
  { id: 'aloe-bath-gelee', type: 'tube-pump', color: '#a8d5ba', accent: '#1a6b4e', label: 'BATH', sublabel: 'GELÉE' },
  { id: 'aloe-jojoba-conditioner', type: 'tube-pump', color: '#03a9f4', accent: '#fff', label: 'ALOE-JOJOBA', sublabel: 'Conditioner' },
  { id: 'aloe-deep-cleansing', type: 'tube-pump', color: '#4db6ac', accent: '#fff', label: 'DEEP CLEANSE', sublabel: 'Body Wash' },

  // Perfumes
  { id: '25th-edition-women', type: 'perfume', color: '#c2185b', accent: '#fff', label: '25TH', sublabel: 'EDITION WOMEN' },
  { id: '25th-edition-men', type: 'perfume', color: '#1565c0', accent: '#fff', label: '25TH', sublabel: 'EDITION MEN' },
];

// Get darker shade
function darken(hex, amount = 0.3) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  const dr = Math.max(0, Math.round(r * (1 - amount)));
  const dg = Math.max(0, Math.round(g * (1 - amount)));
  const db = Math.max(0, Math.round(b * (1 - amount)));
  return `#${dr.toString(16).padStart(2, '0')}${dg.toString(16).padStart(2, '0')}${db.toString(16).padStart(2, '0')}`;
}

// SVG generators per type
function svgHeader(p) {
  const dark = darken(p.color);
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fafbfa"/>
      <stop offset="100%" stop-color="#eef2ee"/>
    </linearGradient>
    <linearGradient id="prod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${p.color}"/>
      <stop offset="100%" stop-color="${dark}"/>
    </linearGradient>
    <linearGradient id="prodDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="${darken(p.color, 0.15)}"/>
      <stop offset="100%" stop-color="${darken(p.color, 0.45)}"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-10%" width="140%" height="130%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="6"/>
      <feOffset dx="0" dy="8"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.25"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="400" height="400" fill="url(#bg)"/>
  <ellipse cx="200" cy="370" rx="100" ry="10" fill="#000" opacity="0.12"/>`;
}

function bottleShape(p) {
  // Like Aloe Vera Gel bottle
  return `
  <g filter="url(#shadow)">
    <rect x="155" y="60" width="90" height="22" rx="4" fill="${darken(p.color, 0.4)}"/>
    <rect x="159" y="80" width="82" height="14" fill="${darken(p.color, 0.55)}"/>
    <path d="M 145 100 L 145 320 Q 145 340, 165 340 L 235 340 Q 255 340, 255 320 L 255 100 Z" fill="url(#prod)"/>
    <ellipse cx="200" cy="100" rx="55" ry="8" fill="${darken(p.color, 0.2)}"/>
    <rect x="155" y="160" width="90" height="120" fill="#fff" opacity="0.95"/>
    <text x="200" y="195" text-anchor="middle" fill="${darken(p.color, 0.5)}" font-family="Arial,sans-serif" font-size="14" font-weight="900">FOREVER</text>
    <line x1="165" y1="205" x2="235" y2="205" stroke="${p.accent}" stroke-width="1"/>
    <text x="200" y="232" text-anchor="middle" fill="${p.color}" font-family="Arial,sans-serif" font-size="${p.label.length > 10 ? 11 : 14}" font-weight="900">${p.label}</text>
    <text x="200" y="252" text-anchor="middle" fill="${darken(p.color, 0.3)}" font-family="Arial,sans-serif" font-size="9">${p.sublabel}</text>
    <line x1="165" y1="265" x2="235" y2="265" stroke="${p.accent}" stroke-width="1" opacity="0.5"/>
  </g>`;
}

function bottleCapShape(p) {
  // Like supplements/capsule bottle
  return `
  <g filter="url(#shadow)">
    <rect x="160" y="55" width="80" height="36" rx="6" fill="${darken(p.color, 0.45)}"/>
    <rect x="160" y="62" width="80" height="3" fill="${darken(p.color, 0.6)}" opacity="0.5"/>
    <rect x="160" y="77" width="80" height="3" fill="${darken(p.color, 0.6)}" opacity="0.5"/>
    <path d="M 150 100 L 150 330 Q 150 345, 165 345 L 235 345 Q 250 345, 250 330 L 250 100 Z" fill="url(#prod)"/>
    <rect x="158" y="150" width="84" height="140" fill="#fff" opacity="0.95"/>
    <text x="200" y="180" text-anchor="middle" fill="${darken(p.color, 0.5)}" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="2">FOREVER</text>
    <line x1="170" y1="190" x2="230" y2="190" stroke="${p.color}" stroke-width="1.2"/>
    <text x="200" y="220" text-anchor="middle" fill="${p.color}" font-family="Arial Black,sans-serif" font-size="${p.label.length > 9 ? 13 : 16}" font-weight="900">${p.label}</text>
    <text x="200" y="245" text-anchor="middle" fill="${darken(p.color, 0.3)}" font-family="Arial,sans-serif" font-size="10" font-style="italic">${p.sublabel}</text>
    <circle cx="200" cy="270" r="14" fill="none" stroke="${p.color}" stroke-width="1.5"/>
    <text x="200" y="275" text-anchor="middle" fill="${p.color}" font-family="Arial,sans-serif" font-size="11" font-weight="700">60</text>
  </g>`;
}

function jarShape(p) {
  return `
  <g filter="url(#shadow)">
    <rect x="120" y="100" width="160" height="22" rx="3" fill="${darken(p.color, 0.45)}"/>
    <rect x="125" y="118" width="150" height="6" fill="${darken(p.color, 0.6)}"/>
    <path d="M 115 124 L 115 320 Q 115 340, 135 340 L 265 340 Q 285 340, 285 320 L 285 124 Z" fill="url(#prod)"/>
    <ellipse cx="200" cy="124" rx="85" ry="8" fill="${darken(p.color, 0.3)}" opacity="0.5"/>
    <rect x="135" y="170" width="130" height="120" fill="#fff" opacity="0.95"/>
    <text x="200" y="200" text-anchor="middle" fill="${darken(p.color, 0.5)}" font-family="Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="2">FOREVER</text>
    <line x1="155" y1="212" x2="245" y2="212" stroke="${p.accent}" stroke-width="1"/>
    <text x="200" y="240" text-anchor="middle" fill="${p.color}" font-family="Arial Black,sans-serif" font-size="${p.label.length > 8 ? 14 : 18}" font-weight="900">${p.label}</text>
    <text x="200" y="262" text-anchor="middle" fill="${darken(p.color, 0.3)}" font-family="Arial,sans-serif" font-size="11">${p.sublabel}</text>
  </g>`;
}

function tubeShape(p) {
  return `
  <g filter="url(#shadow)">
    <ellipse cx="200" cy="80" rx="14" ry="6" fill="${darken(p.color, 0.5)}"/>
    <rect x="186" y="74" width="28" height="20" fill="${darken(p.color, 0.5)}"/>
    <ellipse cx="200" cy="94" rx="14" ry="3" fill="${darken(p.color, 0.4)}"/>
    <path d="M 165 100 L 235 100 L 245 320 Q 245 345, 220 345 L 180 345 Q 155 345, 155 320 Z" fill="url(#prod)"/>
    <rect x="170" y="155" width="60" height="160" fill="#fff" opacity="0.95"/>
    <text x="200" y="185" text-anchor="middle" fill="${darken(p.color, 0.5)}" font-family="Arial,sans-serif" font-size="10" font-weight="700" letter-spacing="1.5">FOREVER</text>
    <line x1="178" y1="195" x2="222" y2="195" stroke="${p.accent}" stroke-width="0.8"/>
    <text x="200" y="225" text-anchor="middle" fill="${p.color}" font-family="Arial Black,sans-serif" font-size="${p.label.length > 8 ? 11 : 13}" font-weight="900">${p.label}</text>
    <text x="200" y="248" text-anchor="middle" fill="${darken(p.color, 0.2)}" font-family="Arial,sans-serif" font-size="9">${p.sublabel}</text>
    <text x="200" y="295" text-anchor="middle" fill="${darken(p.color, 0.4)}" font-family="Arial,sans-serif" font-size="8" font-style="italic">100ml</text>
  </g>`;
}

function tubePumpShape(p) {
  return `
  <g filter="url(#shadow)">
    <rect x="190" y="50" width="20" height="30" fill="${darken(p.color, 0.5)}"/>
    <rect x="180" y="78" width="40" height="14" rx="3" fill="${darken(p.color, 0.4)}"/>
    <rect x="155" y="92" width="90" height="20" fill="${darken(p.color, 0.3)}"/>
    <path d="M 150 110 L 250 110 L 250 330 Q 250 345, 235 345 L 165 345 Q 150 345, 150 330 Z" fill="url(#prod)"/>
    <rect x="162" y="155" width="76" height="160" fill="#fff" opacity="0.95"/>
    <text x="200" y="185" text-anchor="middle" fill="${darken(p.color, 0.5)}" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="2">FOREVER</text>
    <line x1="172" y1="195" x2="228" y2="195" stroke="${p.accent}" stroke-width="1"/>
    <text x="200" y="230" text-anchor="middle" fill="${p.color}" font-family="Arial Black,sans-serif" font-size="${p.label.length > 9 ? 13 : 15}" font-weight="900">${p.label}</text>
    <text x="200" y="252" text-anchor="middle" fill="${darken(p.color, 0.3)}" font-family="Arial,sans-serif" font-size="10">${p.sublabel}</text>
    <line x1="172" y1="270" x2="228" y2="270" stroke="${p.accent}" stroke-width="1" opacity="0.4"/>
  </g>`;
}

function sprayShape(p) {
  return `
  <g filter="url(#shadow)">
    <rect x="186" y="55" width="28" height="12" fill="${darken(p.color, 0.6)}"/>
    <path d="M 195 67 L 205 67 L 207 80 L 193 80 Z" fill="${darken(p.color, 0.5)}"/>
    <rect x="180" y="80" width="40" height="14" rx="2" fill="${darken(p.color, 0.4)}"/>
    <path d="M 150 95 L 250 95 L 250 335 Q 250 345, 240 345 L 160 345 Q 150 345, 150 335 Z" fill="url(#prod)"/>
    <rect x="160" y="150" width="80" height="160" fill="#fff" opacity="0.95"/>
    <text x="200" y="180" text-anchor="middle" fill="${darken(p.color, 0.5)}" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="2">FOREVER</text>
    <line x1="170" y1="192" x2="230" y2="192" stroke="${p.accent}" stroke-width="1"/>
    <text x="200" y="225" text-anchor="middle" fill="${p.color}" font-family="Arial Black,sans-serif" font-size="${p.label.length > 9 ? 13 : 15}" font-weight="900">${p.label}</text>
    <text x="200" y="248" text-anchor="middle" fill="${darken(p.color, 0.3)}" font-family="Arial,sans-serif" font-size="10">${p.sublabel}</text>
  </g>`;
}

function boxShape(p) {
  return `
  <g filter="url(#shadow)">
    <polygon points="280,90 320,70 320,310 280,330" fill="url(#prodDark)"/>
    <polygon points="120,90 280,90 320,70 160,70" fill="${darken(p.color, 0.2)}"/>
    <rect x="120" y="90" width="160" height="240" fill="url(#prod)"/>
    <rect x="135" y="110" width="130" height="2" fill="${p.accent}" opacity="0.7"/>
    <text x="200" y="140" text-anchor="middle" fill="${p.accent}" font-family="Arial,sans-serif" font-size="12" font-weight="700" letter-spacing="2">FOREVER</text>
    <text x="200" y="155" text-anchor="middle" fill="${p.accent}" font-family="Arial,sans-serif" font-size="9" letter-spacing="3" opacity="0.85">LIVING</text>
    <line x1="160" y1="170" x2="240" y2="170" stroke="${p.accent}" stroke-width="0.5" opacity="0.5"/>
    <text x="200" y="225" text-anchor="middle" fill="${p.accent}" font-family="Georgia,serif" font-size="${p.label.length > 8 ? 28 : 36}" font-weight="900">${p.label}</text>
    <text x="200" y="255" text-anchor="middle" fill="${p.accent}" font-family="Georgia,serif" font-size="14" font-style="italic" opacity="0.95">${p.sublabel}</text>
    <rect x="135" y="310" width="130" height="2" fill="${p.accent}" opacity="0.7"/>
  </g>`;
}

function perfumeShape(p) {
  return `
  <g filter="url(#shadow)">
    <ellipse cx="200" cy="60" rx="24" ry="8" fill="${darken(p.color, 0.6)}"/>
    <rect x="176" y="60" width="48" height="22" rx="3" fill="${darken(p.color, 0.45)}"/>
    <ellipse cx="200" cy="82" rx="24" ry="6" fill="${darken(p.color, 0.5)}"/>
    <path d="M 175 90 L 225 90 L 230 100 L 270 130 Q 280 140, 280 155 L 280 320 Q 280 340, 260 340 L 140 340 Q 120 340, 120 320 L 120 155 Q 120 140, 130 130 L 170 100 Z" fill="url(#prod)"/>
    <rect x="145" y="170" width="110" height="140" fill="#fff" opacity="0.96"/>
    <text x="200" y="220" text-anchor="middle" fill="${p.color}" font-family="Georgia,serif" font-size="48" font-weight="900">${p.label}</text>
    <line x1="160" y1="240" x2="240" y2="240" stroke="${p.color}" stroke-width="1"/>
    <text x="200" y="265" text-anchor="middle" fill="${darken(p.color, 0.3)}" font-family="Arial,sans-serif" font-size="11" letter-spacing="3">${p.sublabel}</text>
    <text x="200" y="290" text-anchor="middle" fill="${darken(p.color, 0.4)}" font-family="Arial,sans-serif" font-size="9" letter-spacing="2">FOREVER</text>
  </g>`;
}

const shapeMap = {
  'bottle': bottleShape,
  'bottle-cap': bottleCapShape,
  'jar': jarShape,
  'tube': tubeShape,
  'tube-pump': tubePumpShape,
  'spray': sprayShape,
  'box': boxShape,
  'perfume': perfumeShape,
};

// Generate all SVGs
const outDir = path.join(__dirname, '../assets/images');
let count = 0;
for (const p of PRODUCTS_CONFIG) {
  const shapeFn = shapeMap[p.type];
  if (!shapeFn) {
    console.log('Unknown type:', p.type);
    continue;
  }
  const svg = svgHeader(p) + shapeFn(p) + '\n</svg>';
  const outPath = path.join(outDir, p.id + '.svg');
  fs.writeFileSync(outPath, svg);
  console.log('Created:', p.id + '.svg');
  count++;
}
console.log(`\nGenerated ${count} SVG product placeholders`);
