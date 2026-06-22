# HARRASSE.SHOP

متجر إلكتروني لمنتجات **Forever Living** الأصلية — تصميم عصري، طلب عبر الواتساب، PWA قابل للتثبيت كتطبيق.

🌐 **اللينك ديال الموقع:** https://harrasse1.github.io/shop/

---

## ✨ المميزات

- 🎨 تصميم فاخر بألوان أخضر/ذهبي
- 🌍 دعم كامل للعربية (RTL) — Cairo / Tajawal
- 📱 متجاوب 100% (جوال + تابلت + حاسوب)
- 🛒 سلة تسوق محفوظة فالـ `localStorage`
- 💬 إرسال الطلب مباشرة عبر **واتساب**
- 🔍 بحث + فرز + فلاتر سريعة (الأكثر مبيعاً / جديد / فالتخفيض)
- 📲 **PWA** — الزبون يقدر يثبت الموقع بحال تطبيق
- ⚡ سريع — HTML/CSS/JS بسيط بلا frameworks ثقيلة
- 🎯 SEO + Open Graph + Schema.org

---

## 🚀 كيفاش تخدّم الموقع على GitHub Pages (مجاناً)

### 1️⃣ فعّل GitHub Pages

1. مشي ل: <https://github.com/harrasse1/shop/settings/pages>
2. تحت **"Source"** → اختار:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
3. كليكي **Save** 💾

### 2️⃣ انتظر دقيقتين

بعد ~2 دقيقة كاتظهر رسالة خضراء:
> ✅ Your site is live at `https://harrasse1.github.io/shop/`

### 3️⃣ شارك اللينك! 🎉

```
https://harrasse1.github.io/shop
```

---

## 🛠️ كيفاش تعدّل أي حاجة

### 💰 تبديل سعر منتج
ملف: `assets/js/products.js` — بدّل قيمة `price` و `oldPrice`.

### ➕ زيادة منتج جديد
ملف: `assets/js/products.js` — زيد بلوك جديد فالقائمة:
```js
{
  id: 'product-jdid',
  image: 'assets/images/sora.webp',
  name: "اسم المنتج",
  cat: 'nutrition',
  catName: "المكملات الغذائية",
  desc: "وصف المنتج...",
  price: 299, oldPrice: 349,
  icon: 'fa-capsules',
  color: '#1a6b4e',
  rating: 5,
  badge: 'new',
},
```

### 📞 تبديل رقم الواتساب
ملف: `assets/js/app.js` — السطر 9:
```js
const WHATSAPP_NUMBER = '212691805347';
```

### 🎨 تبديل الألوان
ملف: `assets/css/style.css` — فالأعلى داخل `:root`.

### 📝 تبديل النصوص (Hero, FAQ, آراء العملاء)
ملف: `index.html`.

---

## 📂 بنية المشروع

```
shop/
├── index.html                  # الصفحة الرئيسية
├── manifest.webmanifest        # إعدادات PWA
├── sw.js                       # Service Worker (PWA)
├── .nojekyll                   # GitHub Pages config
├── assets/
│   ├── css/style.css           # التنسيقات
│   ├── js/
│   │   ├── products.js         # كتالوج المنتجات (39 منتج)
│   │   └── app.js              # منطق السلة والواتساب
│   └── images/                 # الصور (logo + product photos)
└── README.md
```

---

## 🧪 التشغيل المحلي

افتح `index.html` مباشرة، أو شغّل خادم محلي:

```bash
python3 -m http.server 8080
# المتصفح: http://localhost:8080
```

---

## 🌐 ربط دومين خاص (اختياري — مدفوع)

إلا فالمستقبل بغيتي دومين بحال `harrasse.shop`:

1. شري الدومين من Namecheap / Cloudflare / GoDaddy (~10$/عام)
2. ف **Settings → Pages → Custom domain** → كتب الدومين
3. ف لوحة DNS ديال الدومين، زيد:
   ```
   A     @     185.199.108.153
   A     @     185.199.109.153
   A     @     185.199.110.153
   A     @     185.199.111.153
   CNAME www   harrasse1.github.io
   ```
4. انتظر 10-30 دقيقة → ✅ شغّال!

---

## 📲 تثبيت الموقع كتطبيق (للزبائن)

### Android (Chrome):
- يدخل للموقع → كاتبان أيقونة **📥 تثبيت** فالأعلى → كليك

### iPhone (Safari):
- يدخل للموقع → زر المشاركة ↑ → **"إضافة إلى الشاشة الرئيسية"**

### Windows/Mac (Chrome/Edge):
- أيقونة 💻 فالـ URL bar → **تثبيت**

---

## 📞 التواصل

- 📱 واتساب: [+212 691 805 347](https://wa.me/212691805347)
- 🌐 الموقع: <https://harrasse1.github.io/shop/>

---

© HARRASSE.SHOP — صُنع بحب فالمغرب 🇲🇦
