import json
import sys
import os

# Ensure we can import from the main directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from broker.broker import MessageBroker

broker = MessageBroker()

test_message = {
    "transcription": """
        Doctor: Good morning! How are you feeling today?
        Patient: Good morning, doctor. I’ve been feeling really tired lately, and I often wake up feeling completely exhausted.
        
        Doctor: I see. Have you been experiencing any stress or anxiety recently?
        Patient: Yes, actually. My job has been really demanding, and I’ve been feeling overwhelmed. Sometimes I feel anxious for no reason.
        
        Doctor: That’s understandable. Have you had any headaches or dizziness?
        Patient: Yes, I get frequent headaches, especially in the mornings. Also, I feel lightheaded sometimes.
        
        Doctor: I see. What about your diet? Are you eating well?
        Patient: Honestly, not really. I’ve been eating a lot of fast food and skipping meals. I’ve also lost weight recently.
        
        Doctor: That could be affecting your energy levels. Have you been exercising?
        Patient: Not much. I used to, but I just don’t have the motivation anymore.
        
        Doctor: I’d like to check your medical history. Have you had any chronic conditions or past health issues?
        Patient: I had anemia a few years ago, and my doctor said I had low vitamin D levels.
        
        Doctor: That’s important to know. I’ll request your medical records to check if there’s any pattern. Also, I’d like to run some blood tests.
        
        Patient: That sounds good. Should I be worried?
        
        Doctor: Not necessarily. But based on your symptoms, I’d recommend talking to a nutrition specialist to improve your diet, and maybe consulting a mental health expert to manage stress better.
        
        Patient: I appreciate that. I’ll follow up with those specialists.
        
        Doctor: Great! In the meantime, try to maintain a balanced diet, drink plenty of water, and get some light exercise. I’ll follow up with your test results soon.
    """,
    "metadata": {"patient_id": "12345",
                 "doctor_id": "D5678",
                 "consultation_type": "general_medicine"
                 }
}

broker.send_message("orchestrator_input", json.dumps(test_message))
print("Test audio message sent to STT queue.")
