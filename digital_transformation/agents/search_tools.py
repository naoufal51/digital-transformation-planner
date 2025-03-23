from typing import List, Dict, Any

from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool


class SearchTools:
    """Collection of search tools for digital transformation research."""
    
    def __init__(self):
        self.search_engine = DuckDuckGoSearchAPIWrapper()
    
    @tool
    async def search_digital_transformation(self, query: str) -> List[Dict[str, str]]:
        """
        Search for digital transformation resources and information.
        
        Args:
            query: The search query related to digital transformation
            
        Returns:
            List of search results with content and URLs
        """
        results = self.search_engine._ddgs_text(query)
        return [{"content": r["body"], "url": r["href"]} for r in results]
    
    @tool
    async def search_industry_trends(self, industry: str) -> List[Dict[str, str]]:
        """
        Search for digital transformation trends in a specific industry.
        
        Args:
            industry: The industry to search for digital transformation trends
            
        Returns:
            List of search results with content and URLs
        """
        query = f"digital transformation trends in {industry} industry"
        results = self.search_engine._ddgs_text(query)
        return [{"content": r["body"], "url": r["href"]} for r in results]
    
    @tool
    async def search_technology_solutions(self, technology: str) -> List[Dict[str, str]]:
        """
        Search for specific technology solutions for digital transformation.
        
        Args:
            technology: The technology to search for (e.g., 'cloud migration', 'AI implementation')
            
        Returns:
            List of search results with content and URLs
        """
        query = f"{technology} for digital transformation case studies and best practices"
        results = self.search_engine._ddgs_text(query)
        return [{"content": r["body"], "url": r["href"]} for r in results]
    
    @tool
    async def search_implementation_challenges(self, challenge: str) -> List[Dict[str, str]]:
        """
        Search for common challenges and solutions in digital transformation.
        
        Args:
            challenge: The specific challenge area (e.g., 'cultural resistance', 'legacy systems')
            
        Returns:
            List of search results with content and URLs
        """
        query = f"overcoming {challenge} in digital transformation"
        results = self.search_engine._ddgs_text(query)
        return [{"content": r["body"], "url": r["href"]} for r in results]


def get_search_tools():
    """Get all search tools instances."""
    tools = SearchTools()
    return [
        tools.search_digital_transformation,
        tools.search_industry_trends,
        tools.search_technology_solutions,
        tools.search_implementation_challenges
    ] 