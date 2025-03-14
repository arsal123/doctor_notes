import logging
from agents.specialized_nlp_processors.config import NLPConfig
from agents.specialized_nlp_processors.base.base_nlp_agent import BaseNLPAgent
from agents.consultation_orchestrator.config import OrchestratorConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GeneralMedicineAgent(BaseNLPAgent):
    """NLP Agent for analyzing general medical issues in transcriptions."""

    def __init__(self):
        super().__init__(
            agent_name="General_Medicine_Agent",
            system_message="""
                You are an AI-powered **General Medicine Doctor** assistant responsible for analyzing **doctor-patient consultation transcripts** and generating structured clinical recommendations.
                Follow standard medical guidelines (CDC, WHO, UpToDate).
                
                ### **Guidelines for Your Responses**
                **Evidence-Based Recommendations** - Your responses must align with standard medical guidelines (**CDC, WHO, UpToDate, PubMed, clinical best practices**).  
                **No Final Diagnosis** - You are NOT a replacement for a human doctor. Instead, provide **possible conditions** for consideration.  
                **Patient Safety First** - If symptoms indicate an **urgent** condition (e.g., chest pain, neurological deficits), **recommend immediate emergency care**.  
                **Structured Clinical Format** - Always return results in **valid JSON format** with predefined keys.
            """,
            model_config=NLPConfig.GENERAL_MEDICINE_MODEL_CONFIG,
            queue_name=OrchestratorConfig.NLP_AGENT_QUEUES["general_medicine"],
            nlp_type="nlp_general"
        )

if __name__ == "__main__":
    agent = GeneralMedicineAgent()
    agent.start()
