# بطاقة الأمل (Hope Card)

نظام لإدارة معلومات المرضى مبني باستخدام FastAPI وMongoDB.

## الميزات

- واجهة مستخدم بسيطة وسهلة الاستخدام
- دعم كامل للغة العربية وتصميم RTL
- إدارة المرضى (إضافة، تعديل، حذف)
- البحث عن المرضى باستخدام رقم التعريف
- عرض معلومات المريض الشخصية والطبية
- إمكانية طباعة بطاقة المريض

## المتطلبات

- Python 3.8+
- متصفح حديث (Chrome, Firefox, Safari, Edge)

## التثبيت

1. قم بنسخ المشروع:

```bash
git clone https://github.com/yourusername/hope-card.git
cd hope-card
```

2. قم بإنشاء بيئة افتراضية وتفعيلها:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. قم بتثبيت المتطلبات:

```bash
pip install -r requirements.txt
```

## تشغيل التطبيق

1. قم بتشغيل التطبيق:

```bash
python run.py
```

2. افتح المتصفح وانتقل إلى `http://localhost:8000`

## الاستخدام

### واجهة المستخدم

- الصفحة الرئيسية: تعرض خيارات للذهاب إلى صفحة البحث أو لوحة التحكم
- صفحة البحث: تسمح للمستخدمين بالبحث عن المرضى باستخدام رقم التعريف
- صفحة عرض البيانات: تعرض معلومات المريض الشخصية والطبية

### لوحة التحكم الإدارية

- عرض قائمة المرضى: يعرض جميع المرضى المسجلين في النظام
- إضافة مريض جديد: نموذج لإضافة مريض جديد مع بياناته الكاملة
- تعديل بيانات المريض: تحديث معلومات المريض
- حذف بيانات المريض: إزالة المريض من قاعدة البيانات

## ملاحظات

- التطبيق يستخدم MongoDB Atlas كقاعدة بيانات سحابية
- يتم الاتصال بقاعدة البيانات تلقائياً عند تشغيل التطبيق

## الهيكل

```
app/
  ├── models/           # نماذج البيانات
  ├── routes/           # مسارات التطبيق
  ├── static/           # ملفات CSS و JavaScript
  │   ├── css/
  │   ├── js/
  │   └── images/
  ├── templates/        # قوالب HTML
  │   ├── admin/
  │   └── user/
  └── main.py           # نقطة الدخول الرئيسية
```

## المساهمة

نرحب بالمساهمات! يرجى اتباع الخطوات التالية:

1. قم بعمل fork للمشروع
2. قم بإنشاء فرع لميزتك (`git checkout -b feature/amazing-feature`)
3. قم بإجراء تغييراتك (`git commit -m 'Add some amazing feature'`)
4. قم بدفع الفرع (`git push origin feature/amazing-feature`)
5. افتح طلب سحب

## الترخيص

هذا المشروع مرخص تحت ترخيص MIT - انظر ملف [LICENSE](LICENSE) للحصول على التفاصيل.

## الاتصال

اسم المطور - [@yourusername](https://twitter.com/yourusername) - email@example.com

رابط المشروع: [https://github.com/yourusername/hope-card](https://github.com/yourusername/hope-card) 