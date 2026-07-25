# VPN Telegram Bot

ربات تلگرام فروش VPN با قابلیت مدیریت پرداخت و اشتراک

## ویژگی‌ها

- ثبت‌نام و ورود کاربران
- نمایش پلن‌های VPN
- پرداخت با کارت به کارت و ارسال رسید
- تایید پرداخت توسط ادمین
- ایجاد خودکار اشتراک VPN
- سیستم پشتیبانی با تیکت
- پنل مدیریت پیشرفته

## نصب و راه‌اندازی

### ۱. کلون کردن پروژه

```bash
git clone <repository-url>
cd vpn-bot
```

### ۲. ایجاد فایل `.env`

```bash
cp .env.example .env
```

سپس مقادیر زیر را پر کنید:

- `BOT_TOKEN`: توکن ربات تلگرام از @BotFather
- `ADMIN_IDS`: آیدی تلگرام ادمین‌ها (با کاما جدا کنید)
- `BANK_NAME`: نام بانک
- `CARD_NUMBER`: شماره کارت
- `ACCOUNT_HOLDER`: به نام
- `SHABA_NUMBER`: شماره شبا

### ۳. اجرا با Docker

```bash
docker-compose up -d
```

### ۴. اجرا بدون Docker

```bash
pip install -r requirements.txt
python -m bot.main
```

## دستورات ربات

### کاربران
- `/start` - شروع و ثبت‌نام
- پلن‌ها - مشاهده پلن‌های موجود
- حساب من - مشاهده وضعیت اشتراک
- پرداخت - پرداخت و ارسال رسید
- پشتیبانی - ایجاد تیکت پشتیبانی

### ادمین
- `/admin` - پنل مدیریت
- تایید/رد پرداخت‌ها
- مشاهده کاربران
- آمار سیستم

## ساختار پروژه

```
vpn-bot/
├── bot/
│   ├── main.py           # نقطه ورود
│   ├── config.py         # تنظیمات
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py     # مدل‌های دیتابیس
│   ├── handlers/
│   │   ├── start.py      # دستور شروع
│   │   ├── plans.py      # مدیریت پلن‌ها
│   │   ├── payment.py    # پرداخت
│   │   ├── account.py    # حساب کاربری
│   │   ├── support.py    # پشتیبانی
│   │   └── admin.py      # پنل ادمین
│   ├── services/
│   └── utils/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## نکات امنیتی

- فایل `.env` را هرگز در گیت قرار ندهید
- از رمزهای عبور قوی استفاده کنید
- دسترسی ادمین را محدود کنید

## لایسنس

MIT License