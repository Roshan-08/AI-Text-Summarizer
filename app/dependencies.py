from app.services.summarizer import SummaryService

summary_service = SummaryService()

def get_summary_service():
    return summary_service