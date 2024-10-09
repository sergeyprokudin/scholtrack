import requests
from typing import List, Optional, Dict, Any

class CitationExplorerAPI:
    """
    A class to interact with the Semantic Scholar API to retrieve and filter citations for papers.
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the CitationExplorerAPI client.

        Args:
            api_key (Optional[str]): Your Semantic Scholar API key, if available.
        """
        self.headers = {"x-api-key": api_key} if api_key else {}

    def get_citations(self, paper_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve the citations of a given paper by its Semantic Scholar paper ID.

        Args:
            paper_id (str): The ID of the paper to retrieve citations for.
            limit (int): The maximum number of citations to retrieve per request (max allowed per API call).

        Returns:
            List[Dict[str, Any]]: A list of citations for the paper.
        """
        citations = []
        offset = 0
        max_citations = 9999  # The limit imposed by Semantic Scholar without an API key.

        while offset < max_citations:
            params = {
                "fields": "title,authors,abstract,citationCount,year,referenceCount,"
                          "influentialCitationCount,venue,fieldsOfStudy,url,externalIds",
                "limit": min(limit, max_citations - offset),  
                "offset": offset,
            }

            response = requests.get(f"{self.BASE_URL}/{paper_id}/citations", headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break

            data = response.json()
            new_citations = data.get("data", [])
            if not new_citations:
                break
            citations.extend(new_citations)

            offset += limit

            # Handle the case where we hit the 10,000 citation limit.
            if offset >= max_citations:
                print(f"WARNING: Paper ID {paper_id} has more than {max_citations} citations. Only the first {max_citations} will be fetched!")
                break

        return citations


    def get_citations_for_papers(self, paper_ids: List[str], cites_at_least_n: int = 0, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Retrieve papers that cite at least `cites_at_least_n` papers from the provided list of paper IDs,
        ensuring that each citation is unique.

        Args:
            paper_ids (List[str]): List of paper IDs to check citations for.
            cites_at_least_n (int): Minimum number of papers from the list that a citing paper must reference.
            limit (int): The maximum number of citations to retrieve per request.

        Returns:
            List[Dict[str, Any]]: A list of unique papers that cite at least `cites_at_least_n` papers from the input list.
        """
        citation_count = {}
        all_citations = []
        unique_citation_ids = set()

        # Gather citations for each paper in the input list
        for paper_id in paper_ids:
            citations = self.get_citations(paper_id, limit=limit)

            # Track how many times each citing paper references papers in the input list
            for citation in citations:
                citing_paper_id = citation.get("citingPaper", {}).get("paperId")
                if citing_paper_id:
                    citation_count[citing_paper_id] = citation_count.get(citing_paper_id, 0) + 1
                    # Ensure we track only unique citations
                    if citing_paper_id not in unique_citation_ids:
                        all_citations.append(citation)
                        unique_citation_ids.add(citing_paper_id)

        # Filter to include only papers that cite at least `cites_at_least_n` papers from the list
        filtered_citations = [
            citation for citation in all_citations
            if citation_count.get(citation.get("citingPaper", {}).get("paperId"), 0) >= cites_at_least_n
        ]

        return filtered_citations

    @staticmethod
    def parse_paper_ids_from_file(filename: str) -> List[str]:
        """
        Parse a file to extract paper IDs, ignoring any comments.

        Args:
            filename (str): The path to the file containing paper IDs and comments.

        Returns:
            List[str]: A list of extracted paper IDs.
        """
        paper_ids = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Split by '#' and take the first part (the paper ID)
                    paper_id = line.split("#")[0].strip()
                    if paper_id:
                        paper_ids.append(paper_id)
        return paper_ids
