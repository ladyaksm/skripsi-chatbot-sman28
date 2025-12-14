from groq import Groq as GroqClient
from config import GROQ_API_KEY
from utils.logger import log_info, log_warning
groq_client = None
GROQ_CLIENT_AVAILABLE = False

def get_groq_client():
    global groq_client, GROQ_CLIENT_AVAILABLE

    if groq_client is not None and GROQ_CLIENT_AVAILABLE:
        return groq_client

    if not GROQ_API_KEY:
        log_info("[INFO] Tidak ada GROQ_API_KEY, skip inisialisasi Groq.")
        return None

    try:
        groq_client = GroqClient(api_key=GROQ_API_KEY)
        GROQ_CLIENT_AVAILABLE = True
        log_info("Groq client aktif")

        return groq_client
    except Exception as e:
        GROQ_CLIENT_AVAILABLE = False
        log_warning(f"[WARNING] Gagal inisialisasi Groq client: {e}")
        return None
