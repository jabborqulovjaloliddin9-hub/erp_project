# O'quv Markazlari uchun Django ERP Tizimi

O'quv markazlari, maktablar yoki akademiyalarni boshqarish uchun **Django** freymvorkida yaratilgan sodda, chiroyli va qulay ERP (Enterprise Resource Planning) veb-ilovasi. Tizimda **Adminlar**, **O'qituvchilar** va **O'quvchilar** uchun alohida boshqaruv panellari (dashboard) mavjud.

---

## 🚀 Asosiy Imkoniyatlar

### 👤 Admin Paneli
- **Bosh sahifa (Dashboard)**: O'quvchilar, o'qituvchilar, guruhlar soni va umumiy daromad statistikasi.
- **Foydalanuvchilarni boshqarish**: O'quvchilar, o'qituvchilar va adminlarni qo'shish, tahrirlash va o'chirish.
- **Guruhlar va Kurslar**: Guruhlar ochish, o'quvchilarni guruhlarga qo'shish va o'qituvchilarni biriktirish.
- **To'lovlar va Hisobotlar**: To'lovlarni nazorat qilish va moliyaviy hisobotlarni ko'rish.
- **Qo'llab-quvvatlash**: O'quvchilar va o'qituvchilardan kelgan murojaat va shikoyatlarga javob berish.

### 👨‍🏫 O'qituvchi Paneli
- **Bosh sahifa**: Faol guruhlar ro'yxati va dars jadvali.
- **Yo'qlama**: Kunlik darslarga o'quvchilarning qatnashishini belgilash (yo'qlama qilish).
- **Vazifalar va Baholash**: O'quvchilarga uy vazifalarini yuklash va ularni baholash.
- **Materiallar**: Guruhlar uchun o'quv materiallari va darsliklarni yuklash.

### 🎓 O'quvchi Paneli
- **Bosh sahifa**: O'zlashtirish, baholar va davomat ko'rsatkichlari.
- **Kurslar va Jadval**: Faol kurslar va haftalik dars jadvalini ko'rish.
- **Uy vazifalari**: Berilgan vazifalarni ko'rish va tayyor topshiriqlarni yuklash.
- **To'lovlar**: To'lovlar tarixi va oylik to'lov holatini tekshirish.

---

## 🛠️ Texnologiyalar
- **Backend (Orqa fon)**: Python, Django
- **Ma'lumotlar bazasi**: SQLite (standart / ishlab chiqish bosqichida)
- **Frontend (Tashqi ko'rinish)**: HTML5, CSS3 (Tailwind CSS)

---

## 💻 Loyihani Kompyuterda Ishga Tushirish

Loyihani o'z kompyuteringizda ishga tushirish uchun quyidagi qadamlarni bajaring:

1. **Repozitoriyani yuklab oling (Clone):**
   ```bash
   git clone https://github.com/username/erp_project.git
   cd erp_project
   ```

2. **Virtual muhitni yaratib, uni faollashtiring:**
   ```bash
   python -m venv .venv
   # Windows (Git Bash terminalida):
   source .venv/Scripts/activate
   # macOS/Linux terminalida:
   source .venv/bin/activate
   ```

3. **Kerakli kutubxonalarni o'rnating:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ma'lumotlar bazasini sozlang (Migrations):**
   ```bash
   python manage.py migrate
   ```

5. **Superuser (Admin akkaunt) yarating:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Serverni ishga tushiring:**
   ```bash
   python manage.py runserver
   ```
   Brauzeringizda [http://127.0.0.1:8000/](http://127.0.0.1:8000/) havolasini oching.
