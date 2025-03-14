from autogen import AssistantAgent, ConversableAgent
config_list = [
    {"model": "gpt-4o-mini-2024-07-18", "api_key": ""},
   # {"model": "gpt-4-turbo", "api_key": "OPENAI_API_KEY"},  # Main doctor agent (general decision-making)
   # {"model": "biogpt", "api_base": "https://custom-llm.com", "api_key": "BIOGPT_KEY"},  # Mental health AI
   # {"model": "clinical-t5", "api_base": "https://custom-llm.com", "api_key": "CLINICALT5_KEY"},  # General medicine AI
   # {"model": "medalpaca", "api_base": "https://custom-llm.com", "api_key": "MEDALPACA_KEY"},  # Nutrition AI
]


#Create conversable agent and control the behaviour of agent
#with a system message(prompt)
member_agent = ConversableAgent(
    name="Member_Agent",
    system_message="You are a patient willing to take advise.",
    llm_config={"config_list": config_list, "seed": 42},
    human_input_mode="NEVER",  # Never ask for human input.
    max_consecutive_auto_reply=1,  # Limit the number of consecutive auto-replies.
)
mentalhealth_agent = AssistantAgent(
    name="MH_Agent",
    system_message="""
    You are a mental health specialist. Your role is to analyze patient symptoms based on their transcript and provide appropriate mental health recommendations.
    Guidelines:
    - If symptoms suggest anxiety, recommend therapy or mindfulness.
    - If sleep issues exist, suggest sleep hygiene improvements.
    - If depression is indicated, suggest consulting a psychiatrist.
    Provide structured recommendations in below JSON format:
    {
      "diagnosis": "Possible Anxiety Disorder",
      "recommendations": ["Cognitive Behavioral Therapy", "Daily Meditation", "Avoid Caffeine"],
      "summary"
    }
    """,
    llm_config={"config_list": config_list, "seed": 42},
)

def get_mental_health_recommendation(transcript):
    return mentalhealth_agent.generate_reply(messages=[{"content": transcript,
                                        "role": "user"
                                        }])


#Asking member agent to initiate the chat to mental health agent
#max_turns tells the agent how many times the agent has to reply to continue the conversation
#chat_result = member_agent.initiate_chat(
#    mentalhealth_agent,
#    message="I think about death all the time",
#    summary_method="reflection_with_llm",
#    max_turns=1,
#)
#print(chat_result)

response = get_mental_health_recommendation("I think about death all the time")
print(response)


# Get the chat history.
#import pprint
#pprint.pprint(chat_result.chat_history)
#chat_result


