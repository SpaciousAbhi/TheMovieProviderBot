
from pyrogram import Client, filters
import datetime
import asyncio
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages, broadcast_messages_group

# Global variable to track if broadcasting should be stopped
stop_broadcast = False

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_to_users(bot, message):
    global stop_broadcast
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    total_users = await db.total_users_count()
    
    sts = await message.reply_text(
        text=f'Starting broadcast to {total_users} users...'
    )
    
    start_time = datetime.datetime.now()
    success = 0
    blocked = 0
    deleted = 0
    failed = 0
    
    for index, user in enumerate(users, start=1):
        if stop_broadcast:
            await sts.edit("Broadcast Cancelled.")
            return
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti is False:
            if sh == "Blocked":
                blocked += 1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        if index % 20 == 0:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users: {total_users}\nCompleted: {index}/{total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\nFailed: {failed}")

    time_taken = datetime.datetime.now() - start_time
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken.total_seconds()} seconds.\n\nTotal Users: {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\nFailed: {failed}")

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_to_groups(bot, message):
    global stop_broadcast
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    total_groups = await db.total_chat_count()
    
    sts = await message.reply_text(
        text=f'Starting broadcast to {total_groups} groups...'
    )
    
    start_time = datetime.datetime.now()
    success = 0
    failed = 0
    
    for index, group in enumerate(groups, start=1):
        if stop_broadcast:
            await sts.edit("Broadcast Cancelled.")
            return
        pti, sh = await broadcast_messages_group(int(group['id']), b_msg)
        if pti:
            success += 1
        elif pti is False:
            failed += 1
        if index % 20 == 0:
            await sts.edit(f"Broadcast in progress:\n\nTotal Groups: {total_groups}\nCompleted: {index}/{total_groups}\nSuccess: {success}\nFailed: {failed}")

    time_taken = datetime.datetime.now() - start_time
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken.total_seconds()} seconds.\n\nTotal Groups: {total_groups}\nSuccess: {success}\nFailed: {failed}")

@Client.on_message(filters.command("cancel_broadcast") & filters.user(ADMINS))
async def cancel_broadcast(bot, message):
    global stop_broadcast
    stop_broadcast = True
    await message.reply_text("Broadcast Cancelled.")
