import os
import json
import base64

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None

def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key or genai is None:
        return None
    return genai.Client(api_key=key)

def _prompt(category, data, budget):
    common = f"""
You are PocketSmart AI, a practical budget recommendation assistant.
Total budget: {budget}
Return ONLY valid JSON with this shape:
{{
  "summary": "short explanation",
  "budget_breakdown": [{{"category":"...", "amount": 0}}],
  "recommendations": [
    {{"name":"...", "platform":"...", "estimated_price":0, "reason":"...", "link":"https://example.com"}}
  ],
  "tips": ["...", "..."]
}}
Do not claim live prices or live availability. Clearly use estimated prices.
Keep the total recommended spend at or below the given budget.
"""
    if category == "home":
        return common + f"""
Plan a home interior setup.
Room: {data.get('room','Living Room')}
Style: {data.get('style','Modern')}
Items/requirements: {data.get('items','lights, decor, furniture')}
Prioritize useful items and split the budget sensibly.
"""
    if category == "party":
        return common + f"""
Plan an event.
Event type: {data.get('event_type','Birthday')}
Guests: {data.get('guests','10')}
Venue preference: {data.get('venue','Home or affordable hall')}
Food preference: {data.get('food','Mixed')}
Decoration: {data.get('decoration','Simple')}
Allocate budget among food, venue and decoration.
"""
    return common + f"""
Plan jewelry for an occasion.
Occasion: {data.get('occasion','Wedding')}
Style: {data.get('style','Elegant')}
Outfit/color notes: {data.get('outfit_notes','Not specified')}
Suggest matching jewelry within budget.
"""

def _fallback(category, data, budget):
    if category == "home":
        parts = [
            ("Lighting", budget*0.15, "Warm LED lights / ceiling light"),
            ("Decor", budget*0.20, "Wall art, plants and cushions"),
            ("Furniture", budget*0.45, "One practical statement furniture item"),
            ("Accessories", budget*0.20, "Curtains, rug or storage"),
        ]
        platform = "Amazon / IKEA / Flipkart"
    elif category == "party":
        parts = [
            ("Food", budget*0.50, "Food and beverages"),
            ("Venue", budget*0.25, "Affordable venue or home setup"),
            ("Decoration", budget*0.15, "Balloons, backdrop and table decor"),
            ("Contingency", budget*0.10, "Buffer for unexpected costs"),
        ]
        platform = "Swiggy / Zomato / Local vendors"
    else:
        parts = [
            ("Earrings", budget*0.25, "Lightweight matching earrings"),
            ("Necklace", budget*0.45, "Main statement necklace"),
            ("Bangles", budget*0.20, "Matching bangles"),
            ("Contingency", budget*0.10, "Buffer"),
        ]
        platform = "Amazon / Flipkart / Local jewellery stores"

    recommendations = [
        {
            "name": name,
            "platform": platform,
            "estimated_price": round(amount),
            "reason": reason,
            "link": "https://www.amazon.in/"
        }
        for name, amount, reason in parts
    ]
    return {
        "summary": f"Demo recommendation created for a {category} plan within your budget.",
        "budget_breakdown": [
            {"category": name, "amount": round(amount)} for name, amount, _ in parts
        ],
        "recommendations": recommendations,
        "tips": [
            "Compare prices before purchasing.",
            "Keep a small contingency amount.",
            "Prices and availability are estimates, not live listings."
        ],
        "mode": "fallback"
    }

def generate_recommendations(category, data, budget, image_bytes=None):
    client = _client()
    if client is None:
        return _fallback(category, data, budget)

    try:
        contents = [_prompt(category, data, budget)]
        if image_bytes and types:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))

        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(model=model, contents=contents)
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        result["mode"] = "gemini"
        return result
    except Exception:
        return _fallback(category, data, budget)
