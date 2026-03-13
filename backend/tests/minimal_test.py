#!/usr/bin/env python3
"""
Minimal test to check if the WhatsApp webhook route works
"""

from fastapi import FastAPI, Request
from starlette.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request):
    """Minimal test route for WhatsApp"""
    try:
        # Parse form data
        form_data = await request.form()

        # Just return a simple TwiML response
        resp = MessagingResponse()
        return Response(content=str(resp), media_type="application/xml")
    except Exception as e:
        print(f"Error: {e}")
        resp = MessagingResponse()
        return Response(content=str(resp), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
