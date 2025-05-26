# Serverless Function: /api/assistant
import os, json
from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

def handler(request):
    """Vercel Python Function entrypoint."""
    try:
        body   = request.json()           # parses JSON body
        prompt = (body.get("prompt") or "").strip()
        if not prompt:
            return {"error": "prompt required"}, 400

        # Call the Responses API + Image tool
        chat = client.responses.create(
            model="gpt-4o-mini",          # cheap default
            input=[{
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}]
            }],
            tools=[{
                "type": "image_generation",
                "quality": "high",
                "output_format": "url"
            }],
            temperature=0.8,
            max_output_tokens=1024,
        )

        msg = chat.output.choices[0].message   # adjust if SDK shape changes
        return {
            "text": msg.content,
            "image_url": getattr(msg, "image_url", None)
        }

    except Exception as e:
        # Simple error surface
        return {"error": str(e)}, 500
