"""
File that contains the logic for the news checklist.
"""
from src.logic.helper_functionality.news_check.news_relevancy_check import RelevancyChecker

class NewsChecklist():
    """
    Class that contains the logic for the news checklist.
    """

    def __init__(self):
        self.relevancyChecker: RelevancyChecker  = RelevancyChecker()

    def checklist(self, news: dict, company: str) -> int:
        """
        Check whether the news checklist for authenticating the news as relevant as 
        well as the source as credible (future) is fulfilled.

        :param news: The news article to check.
        :return: 0 if the conditions are fulfilled, 1 otherwise.
        """
        result: int = self.relevancyChecker.check_relevancy(company = company, news = news["body"]) 
        return result