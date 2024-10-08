import json
import csv
from typing import List, Dict, Any

class CitationExporter:
    """
    A class to handle exporting citations to different formats.
    """

    @staticmethod
    def save_to_json(data: List[Dict[str, Any]], filename: str = "citations.json") -> None:
        """
        Save data to a JSON file.

        Args:
            data (List[Dict[str, Any]]): The data to save.
            filename (str): The name of the JSON file.
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def save_to_csv(citations: List[Dict[str, Any]], filename: str = "citations.csv", sort_by: str = "citations") -> None:
        """
        Save citations to a CSV file.

        Args:
            citations (List[Dict[str, Any]]): The list of citations to save.
            filename (str): The name of the CSV file.
            sort_by (str): The field by which to sort the citations (citation_count, year, or arxiv).
        """
        valid_sort_options = {"citations", "year", "arxiv"}
        if sort_by not in valid_sort_options:
            raise ValueError(f"Invalid sort option. Please use one of {valid_sort_options}")

        citations_sorted = sorted(citations, key=lambda x: CitationExporter.get_sort_value(x, sort_by), reverse=True)

        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            fieldnames = [
                "title", "year", "citation_count", "arxiv_url", "authors", "abstract", "venue", "paper_id", "semantic_scholar_url"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for citation in citations_sorted:
                citing_paper = citation.get("citingPaper", {})
                external_ids = citing_paper.get("externalIds", {})
                arxiv_url = f"https://arxiv.org/abs/{external_ids.get('ArXiv', '')}" if external_ids.get("ArXiv") else "N/A"

                row = {
                    "title": citing_paper.get("title", "N/A"),
                    "authors": ", ".join([author["name"] for author in citing_paper.get("authors", [])]),
                    "abstract": citing_paper.get("abstract", "N/A"),
                    "year": citing_paper.get("year", 0),
                    "citation_count": citing_paper.get("citationCount", 0),
                    "venue": citing_paper.get("venue", "N/A"),
                    "paper_id": citing_paper.get("paperId", "N/A"),
                    "arxiv_url": arxiv_url,
                    "semantic_scholar_url": citing_paper.get("url", "N/A")
                }
                writer.writerow(row)

    @staticmethod
    def get_sort_value(citation: Dict[str, Any], sort_by: str) -> Any:
        """
        Extract the sort value from a citation based on the specified field.

        Args:
            citation (Dict[str, Any]): The citation to extract the sort value from.
            sort_by (str): The field to sort by.

        Returns:
            Any: The value to be used for sorting.
        """
        citing_paper = citation.get("citingPaper", {})
        if sort_by == "citations":
            return citing_paper.get("citationCount", 0) or 0
        elif sort_by == "year":
            return citing_paper.get("year", 0) or 0
        elif sort_by == "arxiv":
            return citing_paper.get("externalIds", {}).get("ArXiv", "")
        return 0

    @staticmethod
    def save_to_txt(citations: List[Dict[str, Any]], filename: str = "citations.txt", sort_by: str = "citations", show_abstract: bool = False) -> None:
        """
        Save citations to a human-readable text file, sorted by the specified field, with an option to skip abstracts.
        """
        citations_sorted = sorted(citations, key=lambda x: CitationExporter.get_sort_value(x, sort_by), reverse=True)
        with open(filename, "w", encoding="utf-8") as txtfile:
            for citation in citations_sorted:
                citing_paper = citation.get("citingPaper", {})
                title = citing_paper.get("title", "N/A")
                authors = citing_paper.get("authors", [])
                author_list = ", ".join([author["name"] for author in authors])
                citation_count = citing_paper.get("citationCount", 0)
                year = citing_paper.get("year", "N/A")
                abstract = citing_paper.get("abstract", "N/A")
                venue = citing_paper.get("venue", "N/A")
                external_ids = citing_paper.get("externalIds", {})
                arxiv_url = f"https://arxiv.org/abs/{external_ids.get('ArXiv', '')}" if external_ids.get("ArXiv") else "N/A"
                semantic_scholar_url = citing_paper.get("url", "N/A")

                txtfile.write(f"Title: {title}\n")
                txtfile.write(f"Authors: {author_list}\n")
                txtfile.write(f"Citation Count: {citation_count}\n")
                txtfile.write(f"Year: {year}\n")
                if show_abstract:
                    txtfile.write(f"Abstract: {abstract}\n")
                txtfile.write(f"Venue: {venue}\n")
                txtfile.write(f"ArXiv URL: {arxiv_url}\n")
                txtfile.write(f"Semantic Scholar URL: {semantic_scholar_url}\n\n")

    @staticmethod
    def display_citations(citations: List[Dict[str, Any]], sort_by: str = "citations", limit: int = 10, show_abstract: bool = False) -> None:
        """
        Display the top `limit` citations in a human-readable format, sorted by the specified field, with an option to skip abstracts.
        """
        citations_sorted = sorted(citations, key=lambda x: CitationExporter.get_sort_value(x, sort_by), reverse=True)

        # Display a header indicating how many results will be shown
        print(f"\nShowing top {min(limit, len(citations))} out of {len(citations)} citations:\n")

        for idx, citation in enumerate(citations_sorted[:limit], start=1):
            citing_paper = citation.get("citingPaper", {})
            title = citing_paper.get("title", "N/A")
            authors = citing_paper.get("authors", [])
            author_list = ", ".join([author["name"] for author in authors])
            citation_count = citing_paper.get("citationCount", 0)
            year = citing_paper.get("year", "N/A")
            abstract = citing_paper.get("abstract", "N/A")
            venue = citing_paper.get("venue", "N/A")
            external_ids = citing_paper.get("externalIds", {})
            arxiv_url = f"https://arxiv.org/abs/{external_ids.get('ArXiv', '')}" if external_ids.get("ArXiv") else "N/A"
            semantic_scholar_url = citing_paper.get("url", "N/A")

            # Print the enumerated citation result
            print(f"{idx}. Title: {title}")
            print(f"   Authors: {author_list}")
            print(f"   Citation Count: {citation_count}")
            print(f"   Year: {year}")
            if show_abstract:
                print(f"   Abstract: {abstract}")
            print(f"   Venue: {venue}")
            print(f"   ArXiv URL: {arxiv_url}")
            print(f"   Semantic Scholar URL: {semantic_scholar_url}\n")
