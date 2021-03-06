from src.db import mongodb


def update(userid, current_state, state_completion, **kwargs):
    if mongodb.cx.caterbot.user.find_one({"fb_id": userid}):
        r = mongodb.cx.caterbot.user.update_one(
            {"fb_id": userid},
            {
                "$set": {
                    "current_state": current_state,
                    "current_state_completed": state_completion,
                    **kwargs,
                }
            },
        )
    return r.matched_count
