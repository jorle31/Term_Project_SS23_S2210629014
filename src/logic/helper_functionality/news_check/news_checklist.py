"""
File that contains the logic for the news checklist.
"""
from src.logic.helper_functionality.news_check.news_relevancy_check import RelevancyChecker

class NewsChecklist():
    """
    Class that contains the logic for the news checklist.
    """

    def __init__(self):
        self.relevancyChecker = RelevancyChecker()

    def checklist(self, news: dict, company: str) -> bool:
        """
        Check whether the news checklist for authenticating the news as relevant as 
        well as the source as credible (future) is fulfilled.

        :param news: The news article to check.
        :return: True if the conditions are fulfilled, False otherwise.
        """
        result: bool = self.relevancyChecker.check_relevancy(company = company, news = news["body"]) 
        return result