import logging

from agents.specialized_nlp_processors.base.base_nlp_agent import BaseNLPAgent
from agents.specialized_nlp_processors.config import NLPConfig
from agents.consultation_orchestrator.config import OrchestratorConfig


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class NutritionNLP(BaseNLPAgent):
    """NLP Agent for analyzing nutrition-related issues in transcriptions."""

    def __init__(self):
        super().__init__(
            agent_name="Nutrition_Agent",
            system_message="""
                            You are a nutritionist. Provide dietary recommendations based on patient conditions and symptoms.
                            Follow standard medical guidelines (CDC, WHO, UpToDate).
                            **Structured Clinical Format** - Always return results in **valid JSON format** with predefined keys.
                           """,
            model_config=NLPConfig.NUTRITION_MODEL_CONFIG,
            queue_name  =OrchestratorConfig.NLP_AGENT_QUEUES['nutrition'],
            nlp_type    ="nlp_nutrition"
        )

if __name__ == "__main__":
    agent = NutritionNLP()
    agent.start()
