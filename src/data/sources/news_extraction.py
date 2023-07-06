"""
File that contains the logic for news extraction.
"""
import logging
from typing import List
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems

from src.logic.config import secrets as config_secrets

class NewsExtractor():
    """
    Class that handles the extraction of news articles from the Event Registry API.
    """

    def __init__(self) -> None:
        """
        Initialize the NewsExtractor.
        """
        self.event_registry = EventRegistry(
            apiKey = config_secrets.read_newsapi_credentials(), allowUseOfArchive=False
        )
        self.news: List[List[dict]] = []

    def get_news(self, keywords: List[str], max_articles: int) -> List[dict]:
        """
        Retrieve the latest news article for a given collection of keywords by querying the Event Registry 
        API sorted by their date.

        :param keywords: A string containing relevant keywords.
        :param max_articles: The maximum number of articles to retrieve.
        :return: A list of news articles for the given keywords.
        :raise ValueError: If arg keywords is not list of strings or if the list is empty.
        :raise ValueError: If arg max_articles is not a positive integer.
        """
        if not isinstance(keywords, List) or not keywords:
            raise ValueError("Argument keywords must be a non-empty List of strings.")
        if not isinstance(max_articles, int) or max_articles <= 0:
            raise ValueError("Argument max_articles must be a positiv integer.")
        try:
            q: QueryArticlesIter = QueryArticlesIter(
                keywords = QueryItems.OR([f'"{keyword}"' for keyword in keywords[:5]]), dataType = ["news", "pr"]
            )
            for article in q.execQuery(
                self.event_registry,
                sortBy = "date",
                sortByAsc = False,
                maxItems = max_articles,
            ):  
                self.news.append(article)
        except Exception as e:
            logging.error(e)
            raise ValueError(f"Error: {str(e)}") from e
        return self.news
