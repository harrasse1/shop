/**
 * Removes products without real photos and adds new uploaded ones.
 * Also updates 3 existing products with newly uploaded images.
 */
const fs = require('fs');

// Load products
const code = fs.readFileSync('./assets/js/products.js', 'utf8');
// Strip the wrapper to evaluate just the array
const arrMatch = code.match(/const PRODUCTS = (\[[\s\S]*?\n\];)/);
if (!arrMatch) { console.error('Could not parse products.js'); process.exit(1); }
const arrStr = arrMatch[1];

// Use eval-ish approach via Function (without trailing wrapper)
const PRODUCTS = eval(arrStr);
console.log('Loaded products:', PRODUCTS.length);

// Update existing products with new uploaded images
const updates = {
  'forever-arctic-sea': 'assets/images/forever-arctic-sea.webp',
  'forever-calcium': 'assets/images/forever-calcium.png',
  'forever-daily': 'assets/images/forever-daily.png',
};
PRODUCTS.forEach(p => {
  if (updates[p.id]) p.image = updates[p.id];
});

// Remove products without real photos (still SVG)
const filtered = PRODUCTS.filter(p => !p.image || !p.image.endsWith('.svg'));
console.log('Removed products:', PRODUCTS.length - filtered.length);

// Add new product: Sérum Hydratant
filtered.push({
  id: 'serum-hydratant',
  image: 'assets/images/serum-hydratant.png',
  name: 'Sérum Hydratant',
  cat: 'skincare',
  catName: 'العناية بالبشرة',
  desc: 'سيروم مرطب فاخر — ترطيب عميق ومتقدم للبشرة، يمنحها نضارة ومرونة طبيعية.',
  price: 399, oldPrice: 449,
  icon: 'fa-droplet',
  color: '#5d8aa8',
  rating: 5, badge: 'new',
});

// Group by category for output
const order = ['drinks','nutrition','bee','skincare','weight','personal','perfumes'];
const grouped = {};
filtered.forEach(p => {
  if (!grouped[p.cat]) grouped[p.cat] = [];
  grouped[p.cat].push(p);
});

// Build new products.js content with proper formatting
let out = `/* =========================================================
   HARRASSE.SHOP — Forever Living Products Catalog
   ========================================================= */

const PRODUCTS = [
`;

const catNames = {
  drinks: 'مشروبات الصبار (DRINKS)',
  nutrition: 'المكملات الغذائية (NUTRITION)',
  bee: 'منتجات النحل (BEE PRODUCTS)',
  skincare: 'العناية بالبشرة (SKINCARE)',
  weight: 'التخسيس والريجيم (WEIGHT)',
  personal: 'العناية الشخصية (PERSONAL)',
  perfumes: 'العطور (PERFUMES)',
};

order.forEach(cat => {
  if (!grouped[cat] || !grouped[cat].length) return;
  out += `  /* ============== ${catNames[cat]} ============== */\n`;
  grouped[cat].forEach(p => {
    out += `  {\n`;
    out += `    id: '${p.id}',\n`;
    out += `    image: '${p.image}',\n`;
    out += `    name: ${JSON.stringify(p.name)},\n`;
    out += `    cat: '${p.cat}',\n`;
    out += `    catName: ${JSON.stringify(p.catName)},\n`;
    out += `    desc: ${JSON.stringify(p.desc)},\n`;
    out += `    price: ${p.price}${p.oldPrice ? `, oldPrice: ${p.oldPrice}` : ''},\n`;
    out += `    icon: '${p.icon}',\n`;
    out += `    color: '${p.color}',\n`;
    out += `    rating: ${p.rating || 5}${p.badge ? `, badge: '${p.badge}'` : ''},\n`;
    out += `  },\n`;
  });
  out += `\n`;
});

out += `];

// Optional: expose to global
if (typeof window !== 'undefined') {
  window.PRODUCTS = PRODUCTS;
}
`;

fs.writeFileSync('./assets/js/products.js', out);
console.log('Final product count:', filtered.length);
console.log('By category:');
order.forEach(cat => {
  if (grouped[cat] || (cat === 'skincare' && filtered.find(p => p.id === 'serum-hydratant'))) {
    const count = grouped[cat] ? grouped[cat].length : 0;
    const adjusted = cat === 'skincare' ? count + 1 : count;
    console.log(`  ${catNames[cat]}: ${adjusted}`);
  }
});
