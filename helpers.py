import logging
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_from_update(input_text) -> dict:
    try:
        message = input_text.message
        user = message.from_user
        chat = message.chat
        data = {
            "user": {
                "first_name": user.first_name,
                "id": user.id,
                "is_bot": user.is_bot,
                "language_code": user.language_code,
                "username": user.username
            },
            "chat": {
                "id": chat.id,
                "is_forum": chat.is_forum,
                "title": chat.title
            },
            "channel_chat_created":message.channel_chat_created,
            "delete_chat_photo":message.delete_chat_photo,
            "group_chat_created":message.group_chat_created,
            "is_topic_message":message.is_topic_message,
            "message_id":message.message_id,
            "message_thread_id":message.message_thread_id,
            "supergroup_chat_created":message.supergroup_chat_created,
            "text":message.text
        }
        return data
    except Exception as e:
        return {"error": str(e)}