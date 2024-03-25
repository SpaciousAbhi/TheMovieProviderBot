
from pyrogram import Client, filters
import datetime
import asyncio
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages, broadcast_messages_group

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_to_users(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text=f'Starting broadcast to {len(users)} users...'
    )
    start_time = datetime.datetime.now()
    total_users = await db.total_users_count()
    success = 0
    blocked = 0
    deleted = 0
    failed = 0

    for index, user in enumerate(users, start=1):
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
        await sts.edit(f"Broadcasting in progress:\n\nTotal Users: {total_users}\nCurrent User: {index}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\nFailed: {failed}")

    time_taken = datetime.datetime.now() - start_time
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken.total_seconds()} seconds.\n\nTotal Users: {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\nFailed: {failed}")

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_to_groups(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text=f'Starting broadcast to {len(groups)} groups...'
    )
    start_time = datetime.datetime.now()
    total_groups = await db.total_chat_count()
    success = 0
    failed = 0

    for index, group in enumerate(groups, start=1):
        pti, sh = await broadcast_messages_group(int(group['id']), b_msg)
        if pti:
            success += 1
        elif pti is False:
            failed += 1
        await sts.edit(f"Broadcasting in progress:\n\nTotal Groups: {total_groups}\nCurrent Group: {index}\nSuccess: {success}\nFailed: {failed}")

    time_taken = datetime.datetime.now() - start_time
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken.total_seconds()} seconds.\n\nTotal Groups: {total_groups}\nSuccess: {success}\nFailed: {failed}")
