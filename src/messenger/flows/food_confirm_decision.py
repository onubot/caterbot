from fbmessenger.quick_replies import QuickReplies, QuickReply


def get_confirmation(item):
    confirm_order = QuickReply(title="হ্যাঁ", payload="CONFIRM_FOOD_ORDER")
    cancel_order = QuickReply(title="না", payload="CANCEL_FOOD_ORDER")

    replies = QuickReplies(quick_replies=[confirm_order, cancel_order])

    text = {"text": f"আইটেম {item['title']} এর দাম পড়বে {item['price']}। কনফার্ম করব?"}

    text["quick_replies"] = replies.to_dict()

    return text
