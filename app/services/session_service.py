from typing import List, Dict, Any
import logging
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger(__name__)

class SessionService:
    def __init__(self):
        self.supabase: Client | None = None
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                logger.info("Supabase client initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not found. Falling back to in-memory storage.")
            self._sessions: Dict[str, List[Dict[str, Any]]] = {}

    def _get_key(self, channel: str, user_id: str, conversation_id: str) -> str:
        uid = user_id or "anonymous"
        return f"{channel}:{uid}:{conversation_id}"

    def get_history(self, channel: str, user_id: str, conversation_id: str) -> List[Dict[str, Any]]:
        key = self._get_key(channel, user_id, conversation_id)
        
        if self.supabase:
            try:
                response = self.supabase.table('sessions').select('history').eq('session_key', key).execute()
                if response.data and len(response.data) > 0:
                    return response.data[0].get('history', [])
                return []
            except Exception as e:
                logger.error(f"Supabase read error: {e}")
                return []
        else:
            return self._sessions.get(key, [])

    def append_message(self, channel: str, user_id: str, conversation_id: str, message: Dict[str, Any]):
        key = self._get_key(channel, user_id, conversation_id)
        
        if self.supabase:
            try:
                # Get current history
                history = self.get_history(channel, user_id, conversation_id)
                history.append(message)
                
                # Upsert new history
                self.supabase.table('sessions').upsert({
                    'session_key': key,
                    'history': history
                }).execute()
            except Exception as e:
                logger.error(f"Supabase write error: {e}")
        else:
            if key not in self._sessions:
                self._sessions[key] = []
            self._sessions[key].append(message)

    def clear_session(self, channel: str, user_id: str, conversation_id: str):
        key = self._get_key(channel, user_id, conversation_id)
        
        if self.supabase:
            try:
                self.supabase.table('sessions').delete().eq('session_key', key).execute()
            except Exception as e:
                logger.error(f"Supabase delete error: {e}")
        else:
            if key in self._sessions:
                del self._sessions[key]

# Singleton instance
session_manager = SessionService()
