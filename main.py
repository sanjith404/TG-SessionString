import os
import asyncio
from aiohttp import web
import pyromod
from pyrogram import Client as PyroClient, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired, PasswordHashInvalid, ApiIdInvalid


from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneCodeExpiredError

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Optional links for buttons
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "https://t.me/ITACHI_404")
SUPPORT_CHANNEL = os.environ.get("SUPPORT_CHANNEL", "https://t.me/ITACHI_404")

# Demo API ID and Hash shown in the second image style if user doesn't want to use their own
DEMO_API_ID = 10079905
DEMO_API_HASH = "if45f251e2e055f26e5c2add8401530"

# Optional banner image URL (you can replace this with any hosted image or file_id)
BANNER_URL = "https://envs.sh/X_-.jpg" # Placeholder aesthetic image

bot = PyroClient("SessionGenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def start_health_server():
    app = web.Application()
    app.router.add_get("/", lambda _: web.Response(text="Bot is running!"))
    app.router.add_get("/ping", lambda _: web.Response(text="pong"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080))).start()

# --- START COMMAND (Matches Image 2 Style) ---
@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(_, message: Message):
    user_name = message.from_user.first_name
    start_text = (
        f"┌───────────────────────\n\n"
        f"│ ◍ **HEY** {user_name}\n"
        f"│ ◍ **I'M** : String Session Bot\n"
        f"└───────────────────────\n\n"
        f"✿ **I'M A SESSION GENERATE BOT.**\n"
        f"❄️ **SUPPORT** - PYROGRAM | TELETHON.\n"
        f"★ **NO ID LOG OUT ISSUE & FULL SECURE.**\n\n"
        f"❖ **POWERED BY** :- **`@ITACHI_404`**"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧬 GENERATE SESSION", callback_data="main_menu_gen")],
        [InlineKeyboardButton("👤 OWNER", url="https://t.me/ITACHI_404")],
        [InlineKeyboardButton("🛠️ SUPPORT", url="https://t.me/Error404modz")],
        [InlineKeyboardButton("📖 BASIC GUIDES", callback_data="basic_guides")]
    ])
    
    try:
        await message.reply_photo(
            photo=BANNER_URL,
            caption=start_text,
            reply_markup=buttons
        )
    except Exception:
        # Fallback text if photo fails to load
        await message.reply(start_text, reply_markup=buttons)

# --- HELP COMMAND ---
@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(_, message: Message):
    help_text = (
        "💡 **String Session Bot Help & Instructions**\n\n"
        "**What is this bot?**\n"
        "This bot helps you generate Pyrogram V2 and Telethon session strings securely in-memory without saving any database or local files.\n\n"
        "**How to use:**\n"
        "1. Click **🧬 GENERATE SESSION** on the start menu.\n"
        "2. Choose whether you want to use **Your Own API ID/Hash** or the **Demo API** provided.\n"
        "3. Select your library type (**Pyrogram**, **Telethon**, **Pyrogram Bot**, or **Telethon Bot**).\n"
        "4. Follow the prompt instructions to enter your Phone Number and OTP.\n"
        "5. The resulting session string will be sent directly to your **Saved Messages** securely!\n\n"
        "**Commands:**\n"
        "• `/start` - Open the main control panel.\n"
        "• `/help` - View this detailed instruction guide.\n"
        "• `/cancel` - Abort any active session generation process."
    )
    await message.reply(help_text)

# --- CALLBACK ROUTING ---
@bot.on_callback_query(filters.regex("cancel_action"))
async def cancel_cb(client: PyroClient, cb: CallbackQuery):
    try:
        client.stop_listen(cb.message.chat.id)
    except Exception:
        pass
    await cb.answer("Operation cancelled.", show_alert=True)
    await cb.message.edit_text("🚫 **Operation cancelled.**")

@bot.on_callback_query(filters.regex("basic_guides"))
async def basic_guides_cb(_, cb: CallbackQuery):
    guide_text = (
        "📖 **Basic Guides & FAQ**\n\n"
        "• **Where do I get my API ID & HASH?**\n"
        "  Visit [my.telegram.org](https://my.telegram.org), log in with your phone number, go to **API development tools**, and create an application.\n\n"
        "• **Is it safe?**\n"
        "  Yes! All generations happen strictly in-memory (`in_memory=True`), and strings are delivered directly to your Telegram Saved Messages. We do not store tokens.\n\n"
        "• **How to format the OTP?**\n"
        "  When prompted for the login code, separate digits with spaces (e.g., `1 2 3 4 5`) to prevent automated Telegram filters from blocking your session."
    )
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("« BACK", callback_data="back_to_start")]])
    await cb.message.edit_caption(caption=guide_text, reply_markup=buttons)

@bot.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_cb(_, cb: CallbackQuery):
    user_name = cb.from_user.first_name
    start_text = (
        f"┌───────────────────────\n\n"
        f"│ ◍ **HEY** {user_name}\n"
        f"│ ◍ **I'M** : String Session Bot\n"
        f"└───────────────────────\n\n"
        f"✿ **I'M A SESSION GENERATE BOT.**\n"
        f"❄️ **SUPPORT** - PYROGRAM | TELETHON.\n"
        f"★ **NO ID LOG OUT ISSUE & FULL SECURE.**\n\n"
        f"❖ **POWERED BY** :- **`@ITACHI_404`** 🔥"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧬 GENERATE SESSION", callback_data="main_menu_gen")],
        [InlineKeyboardButton("👤 OWNER", url=OWNER_USERNAME),
         InlineKeyboardButton("🛠️ SUPPORT", url=SUPPORT_CHANNEL)],
        [InlineKeyboardButton("📖 BASIC GUIDES", callback_data="basic_guides")]
    ])
    await cb.message.edit_caption(caption=start_text, reply_markup=buttons)

@bot.on_callback_query(filters.regex("main_menu_gen"))
async def main_menu_gen_cb(_, cb: CallbackQuery):
    # Matches Image 1 Style: Option to use Demo API or custom API
    text = (
        "★ **CLICK BELOW BUTTON TO START GEN SESSION.**\n\n"
        "⚙️ **API SELECTION OPTION:**\n"
        "You can use our default demo API credentials or provide your own custom API ID & Hash.\n\n"
        "» **CHOOSE AN OPTION BELOW** ✓"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 USE DEMO API", callback_data="api_demo"),
         InlineKeyboardButton("🛠️ USE CUSTOM API", callback_data="api_custom")],
        [InlineKeyboardButton("« BACK", callback_data="back_to_start")]
    ])
    await cb.message.edit_caption(caption=text, reply_markup=buttons)

@bot.on_callback_query(filters.regex("api_demo"))
async def api_demo_cb(_, cb: CallbackQuery):
    text = (
        "★ **DEMO API SELECTED**\n\n"
        f"• **API ID :-** `{DEMO_API_ID}`\n"
        f"• **API HASH :-** `{DEMO_API_HASH}`\n\n"
        "» **CHOOSE ONE THAT YOU WANT TO GENERATE SESSION** ✓"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎴 TELETHON", callback_data="gen_telethon_demo"),
         InlineKeyboardButton("🚀 PYROGRAM", callback_data="gen_pyrogram_demo")],
        [InlineKeyboardButton("« BACK", callback_data="main_menu_gen")]
    ])
    await cb.message.edit_caption(caption=text, reply_markup=buttons)

@bot.on_callback_query(filters.regex("api_custom"))
async def api_custom_cb(_, cb: CallbackQuery):
    chat_id = cb.message.chat.id
    await cb.message.delete() # Clear photo menu to start text prompts
    await start_generation_flow(bot, chat_id, custom_api=True)

@bot.on_callback_query(filters.regex(r"^gen_(pyrogram|telethon|pyrogram_bot|telethon_bot)_demo$"))
async def demo_generation_callback(client: PyroClient, cb: CallbackQuery):
    lib_type = cb.data.replace("gen_", "").replace("_demo", "")
    chat_id = cb.message.chat.id
    await cb.message.delete()
    await execute_generation(client, chat_id, lib_type, DEMO_API_ID, DEMO_API_HASH)

# --- GENERATION FLOW HANDLER ---
async def start_generation_flow(client: PyroClient, chat_id: int, custom_api: bool):
    try:
        if custom_api:
            api_id_msg = await client.ask(chat_id, "1️⃣ **Send your API ID:**\n*(Send /cancel to abort)*", timeout=180)
            if api_id_msg.text.startswith("/"): return
            try:
                user_api_id = int(api_id_msg.text.strip())
            except ValueError:
                return await client.send_message(chat_id, "❌ **API ID must be an integer number. Start over with /start.**")

            api_hash_msg = await client.ask(chat_id, "2️⃣ **Send your API HASH:**", timeout=180)
            if api_hash_msg.text.startswith("/"): return
            user_api_hash = api_hash_msg.text.strip()
        else:
            user_api_id = DEMO_API_ID
            user_api_hash = DEMO_API_HASH

        # Prompt library type if custom API was chosen
        if custom_api:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎴 TELETHON", callback_data=f"sel_telethon_{user_api_id}_{user_api_hash}"),
                 InlineKeyboardButton("🚀 PYROGRAM", callback_data=f"sel_pyrogram_{user_api_id}_{user_api_hash}")],
            ])
            await client.send_message(chat_id, "» **CHOOSE ONE THAT YOU WANT TO GENERATE SESSION** ✓", reply_markup=buttons)
            return

    except asyncio.TimeoutError:
        await client.send_message(chat_id, "**Process timed out. Start again with /start.**")
    except Exception as e:
        await client.send_message(chat_id, f"**Error:** `{str(e)}`")

@bot.on_callback_query(filters.regex(r"^sel_(pyrogram|telethon|pyrogram_bot|telethon_bot)_(.+)_(.+)"))
async def custom_selection_callback(client: PyroClient, cb: CallbackQuery):
    data_parts = cb.data.split("_")
    # format: sel_pyrogram_or_telethon_or_bot _ api_id _ api_hash
    # handling possible multi-part names like telethon_bot
    if "bot" in cb.data:
        if "pyrogram" in cb.data:
            lib_type = "pyrogram_bot"
        else:
            lib_type = "telethon_bot"
        parts = cb.data.replace("sel_", "").replace(f"{lib_type}_", "").rsplit("_", 1)
    else:
        if "pyrogram" in cb.data:
            lib_type = "pyrogram"
        else:
            lib_type = "telethon"
        parts = cb.data.replace("sel_", "").replace(f"{lib_type}_", "").rsplit("_", 1)
        
    user_api_id = int(parts[0].replace(f"{lib_type}_", ""))
    user_api_hash = parts[1]
    
    chat_id = cb.message.chat.id
    await cb.message.delete()
    await execute_generation(client, chat_id, lib_type, user_api_id, user_api_hash)

# --- CORE GENERATION & AUTH LOGIC ---
async def execute_generation(client: PyroClient, chat_id: int, lib_type: str, api_id: int, api_hash: str):
    user_client = None
    try:
        phone_msg = await client.ask(chat_id, "3️⃣ **Send your Phone Number with Country Code:**\n*(Example: `+919876543210`)*", timeout=180)
        if phone_msg.text.startswith("/"): return
        phone_number = phone_msg.text.strip()

        status_msg = await client.send_message(chat_id, "⏳ **Connecting to Telegram servers...**")

        # 1. Pyrogram User Account Session
        if lib_type == "pyrogram":
            user_client = PyroClient(f"temp_{chat_id}", api_id=api_id, api_hash=api_hash, in_memory=True)
            await user_client.connect()
            sent_code = await user_client.send_code(phone_number)

            otp_msg = await client.ask(chat_id, "4️⃣ **Send the OTP:**\n*(Format: `1 2 3 4 5` with spaces)*", timeout=180)
            if otp_msg.text.startswith("/"): return
            otp = otp_msg.text.replace(" ", "").strip()

            try:
                await user_client.sign_in(phone_number, sent_code.phone_code_hash, otp)
            except SessionPasswordNeeded:
                pwd_msg = await client.ask(chat_id, "🔒 **2FA Enabled! Send your cloud password:**", timeout=180)
                if pwd_msg.text.startswith("/"): return
                await user_client.check_password(pwd_msg.text.strip())
                await pwd_msg.delete()

            session_string = await user_client.export_session_string()
            await user_client.send_message("me", f"🔐 **Your Pyrogram V2 Session:**\n\n`{session_string}`\n\n⚠️ *Keep this secret!*")
            await user_client.disconnect()

        # 2. Pyrogram Bot Token Session
        elif lib_type == "pyrogram_bot":
            token_msg = await client.ask(chat_id, "🤖 **Send your Bot Token** (from @BotFather):", timeout=180)
            if token_msg.text.startswith("/"): return
            bot_token_str = token_msg.text.strip()
            
            user_client = PyroClient(f"temp_bot_{chat_id}", api_id=api_id, api_hash=api_hash, bot_token=bot_token_str, in_memory=True)
            await user_client.start()
            session_string = await user_client.export_session_string()
            await user_client.send_message("me", f"🤖 **Your Pyrogram Bot Session:**\n\n`{session_string}`\n\n⚠️ *Keep this secret!*")
            await user_client.stop()

        # 3. Telethon User Account Session
        elif lib_type == "telethon":
            user_client = TelegramClient(StringSession(), api_id, api_hash)
            await user_client.connect()
            sent_code = await user_client.send_code_request(phone_number)

            otp_msg = await client.ask(chat_id, "4️⃣ **Send the OTP:**\n*(Format: `1 2 3 4 5` with spaces)*", timeout=180)
            if otp_msg.text.startswith("/"): return
            otp = otp_msg.text.replace(" ", "").strip()

            try:
                await user_client.sign_in(phone_number, otp, phone_code_hash=sent_code.phone_code_hash)
            except SessionPasswordNeededError:
                pwd_msg = await client.ask(chat_id, "🔒 **2FA Enabled! Send your cloud password:**", timeout=180)
                if pwd_msg.text.startswith("/"): return
                await user_client.sign_in(password=pwd_msg.text.strip())
                await pwd_msg.delete()

            session_string = user_client.session.save()
            await user_client.send_message("me", f"🔐 **Your Telethon Session:**\n\n`{session_string}`\n\n⚠️ *Keep this secret!*")
            await user_client.disconnect()

        # 4. Telethon Bot Token Session
        elif lib_type == "telethon_bot":
            token_msg = await client.ask(chat_id, "🤖 **Send your Bot Token** (from @BotFather):", timeout=180)
            if token_msg.text.startswith("/"): return
            bot_token_str = token_msg.text.strip()
            
            user_client = TelegramClient(StringSession(), api_id, api_hash)
            await user_client.start(bot_token=bot_token_str)
            session_string = user_client.session.save()
            await user_client.send_message("me", f"🤖 **Your Telethon Bot Session:**\n\n`{session_string}`\n\n⚠️ *Keep this secret!*")
            await user_client.disconnect()

        await status_msg.delete()
        
        # Final Delivery & Auto-Delete Timer
        final_msg = await client.send_message(
            chat_id,
            "✅ **Session Generated Successfully!**\n\n"
            "📩 The string has been sent to your **Saved Messages**.\n"
            f"Here is a temporary copy:\n`{session_string}`\n\n"
            "🧨 *This message will self-destruct in 60 seconds for your security.*"
        )
        
        await asyncio.sleep(60)
        await final_msg.delete()

    except ApiIdInvalid:
        await client.send_message(chat_id, "❌ **Invalid API ID / API HASH combination.**")
    except (PhoneCodeInvalid, PhoneCodeExpired, PhoneCodeInvalidError, PhoneCodeExpiredError):
        await client.send_message(chat_id, "❌ **Invalid or expired OTP code.**")
    except (PasswordHashInvalid, SessionPasswordNeededError):
        await client.send_message(chat_id, "❌ **Incorrect 2FA password.**")
    except asyncio.TimeoutError:
        await client.send_message(chat_id, "**Session timed out. Start again with /start.**")
    except Exception as e:
        await client.send_message(chat_id, f"❌ **Authentication Failed:**\n`{str(e)}`")
    finally:
        try:
            if user_client and hasattr(user_client, "is_connected") and user_client.is_connected:
                await user_client.disconnect()
        except Exception:
            pass

@bot.on_message(filters.command("cancel") & filters.private)
async def cancel_cmd(client: PyroClient, message: Message):
    try:
        client.stop_listen(message.chat.id)
    except Exception:
        pass
    await message.reply("🚫 **Session generation cancelled.**")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_health_server())
    bot.run()
