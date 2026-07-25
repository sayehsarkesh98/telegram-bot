"""
Telegram Bot - Deployed on Render.com
Single file with webhooks + health check
"""
import os
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, Update
from aiogram.filters import CommandStart, Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "my-secret")

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ==================== BOT SETUP ====================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ==================== HANDLERS ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    await message.answer(
        "سلام! ربات با موفقیت روی Render فعال شد ✅\n"
        "Hello! Your bot is live 24/7 on Render.com.\n\n"
        "برای راهنما /help را بزنید.\n"
        "Type /help for commands."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    await message.answer(
        "📋 دستورات ربات / Bot Commands:\n\n"
        "/start - شروع / Welcome\n"
        "/help - راهنما / Help\n"
        "/ping - تست اتصال / Connection test\n\n"
        "هر متنی بفرستید، اکو می‌شود.\n"
        "Send any text and it will be echoed back."
    )

@router.message(Command("ping"))
async def cmd_ping(message: Message):
    """Handle /ping command"""
    await message.answer("pong 🏓")

@router.message(F.text)
async def echo(message: Message):
    """Echo any text message"""
    await message.answer(f"🔁 {message.text}")

# ==================== WEBHOOK SETUP ====================

async def on_startup(app: web.Application):
    """Set webhook on startup"""
    if WEBHOOK_URL:
        webhook_full_url = f"{WEBHOOK_URL}/webhook"
        await bot.set_webhook(
            url=webhook_full_url,
            secret_token=WEBHOOK_SECRET,
        )
        logger.info(f"Webhook set to: {webhook_full_url}")
    else:
        logger.warning("No WEBHOOK_URL set - bot won't receive updates!")

async def on_shutdown(app: web.Application):
    """Cleanup on shutdown"""
    await bot.session.close()
    logger.info("Bot shutdown complete")

# ==================== HEALTH CHECK ====================

async def health_check(request):
    """Health check endpoint for Render"""
    return web.json_response({"status": "ok", "bot": "running"})

# ==================== AIOHTTP APP ====================

app = web.Application()

# Register webhook handler
webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=WEBHOOK_SECRET,
)
webhook_handler.register(app, path="/webhook")

# Register health check
app.router.add_get("/health", health_check)
app.router.add_get("/", health_check)

# Register startup/shutdown hooks
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# ==================== MAIN ====================

if __name__ == "__main__":
    logger.info(f"Starting bot on port {PORT}")
    logger.info(f"BOT_TOKEN set: {bool(BOT_TOKEN)}")
    logger.info(f"WEBHOOK_URL: {WEBHOOK_URL or 'NOT SET'}")
    web.run_app(app, host="0.0.0.0", port=PORT)