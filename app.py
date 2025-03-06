import bittensor as bt
import json
import time
import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from front import FRONTEND_TEMPLATE
from get_related_uids_in_subnet import get_related_uids_in_subnet

TEMPO_BLOCKS = 360 # tempo blocks_in_subnet
SESSION_WINDOW_BLOCKS = TEMPO_BLOCKS * 5 # session window blocks
BLOCK_IN_SECONDS = 12 # block in seconds
AVAILABLE_COMPETITIONS = [
    "accuracy",
    "accuracy", 
    "seo",
    "balanced"
]

app = FastAPI()

class Tensor:
    def __init__(self):
        self.subtensor = bt.subtensor(network="local")
    
    def get_current_session_info(self):
        block = self.subtensor.get_current_block()
        session = block // SESSION_WINDOW_BLOCKS
        # Define available competition types
        current_index = int(session % len(AVAILABLE_COMPETITIONS))
        current_competition = AVAILABLE_COMPETITIONS[current_index]
        current_datetime = time.strftime(
            '%Y-%m-%d %H:%M:%S', 
            time.gmtime(time.time())
        )
        elapsed_blocks = block - (session * SESSION_WINDOW_BLOCKS)
        session_start_time = time.time() - (elapsed_blocks * BLOCK_IN_SECONDS)
        session_start_datetime = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.gmtime(session_start_time)
        )
        
        # Calculate hours, minutes, seconds ago
        time_diff = time.time() - session_start_time
        hours = int(time_diff // 3600)
        minutes = int((time_diff % 3600) // 60)
        seconds = int(time_diff % 60)
        time_ago = f"{hours}h {minutes}m {seconds}s"
        
        session_start_datetime = f"{session_start_datetime} - {time_ago} ago"
        session_end_time = session_start_time + (SESSION_WINDOW_BLOCKS * BLOCK_IN_SECONDS)
        session_end_datetime = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.gmtime(session_end_time)
        )
        # Calculate hours, minutes, seconds until end
        time_until_end = session_end_time - time.time()
        hours = int(time_until_end // 3600)
        minutes = int((time_until_end % 3600) // 60)
        seconds = int(time_until_end % 60)
        time_after = f"{hours}h {minutes}m {seconds}s"
        session_end_datetime = f"{session_end_datetime} - after {time_after}"

        return {
            "session": session,
            "current_competition": current_competition,
            "current_datetime": current_datetime,
            "session_start_datetime": session_start_datetime,
            "session_end_datetime": session_end_datetime
        }

    def get_related_uids(self, subnet_uid: int, uid: int):
        try:
            return get_related_uids_in_subnet(self.subtensor, subnet_uid, uid)
        except Exception as e:
            bt.logging.error(f"Error getting related uids: {e}")
            return {
                "error": str(e)
            }

tensor = Tensor()

@app.get("/session")
def read_session():
    return tensor.get_current_session_info()


@app.get("/")
def read_root():
    info = tensor.get_current_session_info()
    return HTMLResponse(
        content=FRONTEND_TEMPLATE.render(
            available_competitions=AVAILABLE_COMPETITIONS,
            info=info
        ),
        media_type="text/html"
    )


@app.get("/related_uids")
def read_related_uids(subnet_uid: int, uid: int):
    return HTMLResponse(
        content=json.dumps(tensor.get_related_uids(subnet_uid, uid)),
        media_type="application/json"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)