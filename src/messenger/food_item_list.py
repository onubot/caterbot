from fbmessenger.templates import ListTemplate
from fbmessenger.elements import Element, Button
import json
import os

food_list = json.load(open(os.path.join(os.getcwd(), "food_sample.json"), "r"))

food_elements = [
    Element(
        title=item["title"],
        item_url="https://example.com",
        image_url=item["image_url"],
        subtitle=item["subtitle"],
        buttons=[
            Button(
                button_type="postback",
                title=f"অর্ডার করুন",
                payload=f"ORDER#{item['food_id']}",
            )
        ],
    )
    for item in food_list["foods"]
]
