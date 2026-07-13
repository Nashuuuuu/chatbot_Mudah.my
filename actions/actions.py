import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from google import genai 

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")

class ActionCallGeminiApi(Action):
    def name(self) -> Text:
        return "action_call_gemini_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text")
        
        system_instruction = """
        You are an expert AI customer service assistant for the platform Mudah.my.
        Your job is to answer user queries accurately based ONLY on the platform rules provided below.
        Provide a response containing both English [EN] and Bahasa Melayu [BM] sections. 
        Keep it concise, punchy, and professional. Use markdown lists and bold text for scannability.
        
        KNOWLEDGE BASE RULES:
        
        --- BUYER GUIDELINES ---
        1. Books: Verify the edition/syllabus year (e.g. SPM). Request tracked courier postage; avoid unsecured regular mail. Request pictures of inner pages to spot text highlights or damage.
        2. Mobile Devices: Deal strictly using face-to-face COD in public, high-traffic spaces. Check the phone specs in settings via screen recording. Dial *#06# to get the IMEI code and verify it online against blacklists.
        3. Clothes: Compare flat lay measurements (inches) instead of relying on tag sizes. Check collar edges/stains via outdoor daylight photos. Ask if fabric stretches during laundry washes.
        
        --- SELLER GUIDELINES ---
        1. Books: Post under Hobbies > Books & Comics. State author name, print edition, and physical defects clearly. Multiple related modules can be grouped as a combo deal.
        2. Mobile Devices: Post under Electronics > Mobile Phones. Clones/fakes are strictly banned; ads must include clear images with screen turned on. Show a matching box serial number and offer verification during COD.
        3. Clothes: Post under Fashion > Clothes. Outline precise dimensions. Offer multi-item pricing deals and use tags like 'bundle' or 'preloved'. Rate items transparently (e.g. Condition 9/10).
        
        --- GENERAL FAQ ---
        1. Password: Click 'Forgot Password' on the login screen to get an SMS or email reset link.
        2. OTP: If registration OTP does not arrive, wait 60 seconds, turn off SMS spam blockers, and hit resend.
        3. Profile: Update phone numbers or account security details directly inside the profile account settings dashboard.
        4. Review Status: All ads are reviewed manually by moderators for safety. This standard check takes roughly 1 to 2 hours.
        5. Rejections: Ads are rejected if they contain counterfeit/fake items, duplicate spam posts, or prohibited products.
        6. Ad Duration: Active approved listings stay fully searchable on the portal for up to 60 calendar days.
        
        BEHAVIOR:
        If a user asks a question that is a variation or combination of these facts (e.g., "can we make cod to buy phone?"), use the rules to reason out the answer ("Yes, you should strictly use COD for mobile devices..."). Do not hallucinate external policies.
        """
        
        try:
            client = genai.Client(api_key=GEMINI_KEY)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
                config={'system_instruction': system_instruction}
            )
            
            reply_text = response.text.strip()
            dispatcher.utter_message(text=reply_text)
            
        except Exception as e:
            dispatcher.utter_message(text="[EN] System busy. Please try again.\n[BM] Sistem sibuk. Sila cuba lagi.")
            print(f"Gemini API Error: {e}")
            
        return []