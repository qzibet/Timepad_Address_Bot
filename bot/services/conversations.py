from asgiref.sync import sync_to_async

from bot.models import UserConversationState


async def get_user_state(chat_id):
    try:
        user_state = await sync_to_async(UserConversationState.objects.get)(user__chat_id=chat_id)
        return user_state.state
    except UserConversationState.DoesNotExist:
        return None

