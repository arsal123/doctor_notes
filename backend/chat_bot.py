from autogen import AssistantAgent
from agents.specialized_nlp_processors.config import NLPConfig

class ChatBotAgent:
    def __init__(self):
        self.chatbot_agent = AssistantAgent(
            name="chatbot_Agent",
            system_message="You are a smart medical AI assistant.",
            llm_config={"config_list": NLPConfig.MENTAL_HEALTH_MODEL_CONFIG, "seed": 42},
        )

    def chat_with_bot(self, patient_id, prompt):
        reference_prompt = f"""
                        You are assisting user ID: {patient_id}. Provide responses accordingly.
                        """
        try:
            response = self.chatbot_agent.generate_reply(
                messages=[{"content": prompt, "role": "user"}]
            )
            return response if response else "AI response unavailable."
        except Exception as e:
            print("Error generating chatbot response:", e)
            return "Chatbot error."