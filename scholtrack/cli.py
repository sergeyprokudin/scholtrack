import argparse
import os
import sys
import time
from pathlib import Path
from threading import Thread, Event
from scholtrack.api import CitationExplorerAPI
from scholtrack.exporter import CitationExporter
import re
import pkg_resources

def rolling_indicator(stop_event):
    """A simple rolling progress indicator to show the process is ongoing."""
    while not stop_event.is_set():
        for symbol in "|/-\\":
            if stop_event.is_set():
                break
            sys.stdout.write(f"\rProcessing... {symbol}")
            sys.stdout.flush()
            time.sleep(0.2)

def print_header():
    """Print a structured header with app information."""
    header = """
╔════════════════════════════════════════════════════════════════════╗
║                ScholTrack: Academic Citation Tracker               ║
╟────────────────────────────────────────────────────────────────────╢
║ Version: 0.1.1                                                     ║
║ License: Apache 2.0                                                ║
║ Repo: https://github.com/sergeyprokudin/scholtrack                 ║
║ Data Source: Semantic Scholar API                                  ║
║ Last Update: October 2024                                          ║
║ Author: Sergey Prokudin (sergey.prokudin@gmail.com)                ║
╚════════════════════════════════════════════════════════════════════╝
"""
    print(header)


# ANSI escape codes for colors
RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
YELLOW_COLOR = '\033[93m'
BLUE_COLOR = '\033[94m'
PURPLE_COLOR = '\033[95m'
DEFAULT_COLOR = '\033[0m'  # Reset color to default

def extract_paper_id(url: str) -> str:
    """
    Extract the paper ID from a Semantic Scholar URL.

    Args:
        url (str): The Semantic Scholar URL to extract the paper ID from.

    Returns:
        str: The extracted paper ID, or an empty string if not found.
    """
    pattern = r"semanticscholar\.org/paper/.+?/([a-f0-9]{40})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return ""


def load_collection_file(collection_name):
    """
    Load a collection of paper IDs from a file, ignoring comments after '#'.

    Args:
        collection_name (str): The name of the collection (without the .txt extension).

    Returns:
        List[str]: A list of paper IDs.
    """
    try:
        # Load the file using pkg_resources to ensure it's accessible within the package
        collection_file = pkg_resources.resource_filename('scholtrack', f'collections/{collection_name}.txt')

        paper_ids = []
        with open(collection_file, 'r') as f:
            for line in f:
                # Remove comments after '#' and strip leading/trailing whitespaces
                line = line.split('#')[0].strip()

                # Validate that the line contains a paper ID (should match Semantic Scholar ID format)
                if re.match(r'^[a-f0-9]{40}$', line):
                    paper_ids.append(line)

        if not paper_ids:
            print(f"Warning: No valid paper IDs found in {collection_name}.txt.")
        return paper_ids

    except FileNotFoundError:
        print(f"Error: Collection file {collection_name}.txt not found.")
        return []
    
def main():
    print_header()

    parser = argparse.ArgumentParser(
        description='ScholTrack Command-Line Interface: Fetch Citations for Papers via Semantic Scholar API',
        epilog='''Usage examples:

        1. Fetch citations for multiple paper IDs and export to CSV:
            scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a 428b663772dba998f5dc6a24488fff1858a0899f -o my_citations.csv -t csv

        2. Fetch and display citations for Paper IDs from a file, sorted by year:
            scholtrack -f nerf.txt -s year -t stdout

        3. Fetch citations for papers in the "nerf" collection, but only display those citing at least 2 papers from the list:
            scholtrack -c nerf -n 2 -t stdout

        4. Fetch and display citations from URLs, exporting results to CSV:
            scholtrack --urls https://www.semanticscholar.org/paper/.../11665dbecb17ef4d3d71b75b8666ce0e61bd43fa -o my_citations.csv -t csv
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-p', '--paper-ids', nargs='+', help='List of paper IDs to get citations for')
    parser.add_argument('-u', '--urls', nargs='+', help='List of Semantic Scholar URLs to get paper IDs from')
    parser.add_argument('-f', '--file', help='Path to the text file with paper IDs and optional comments')
    parser.add_argument('-c', '--collection', help='Name of the collection (automatically looks in collections/ folder in the repository)')
    parser.add_argument('-n', '--cites-at-least-n', type=int, default=0, help='Minimum number of papers a citing paper must reference from the provided list')
    parser.add_argument('-t', '--output-type', choices=['stdout', 'csv', 'json', 'txt'], default='csv', help='Specify the output format: stdout, csv, json, or txt')
    parser.add_argument('-o', '--output', help='Output file name for csv, json, or txt formats')
    parser.add_argument('-s', '--sort-by', choices=['citations', 'arxiv', 'year'], default='citations', help='Specify the field by which to sort the citations')
    parser.add_argument('--show-abstract', action='store_true', help='Show the abstract field when saving or displaying results')
    parser.add_argument('-q', '--quiet', action='store_true', help='Omit displaying first N citations in the command line')
    parser.add_argument('-k', '--api-key', help='Semantic Scholar API Key (optional)')
    parser.add_argument('-l', '--display-limit', type=int, default=5, help='Maximum number of found papers to show in terminal')

    args = parser.parse_args()

    # Collect paper IDs from input arguments
    paper_ids = []

    # Fetch paper IDs from URLs
    if args.urls:
        for url in args.urls:
            paper_id = extract_paper_id(url)
            if paper_id:
                paper_ids.append(paper_id)
            else:
                print(f"Warning: Unable to extract paper ID from URL {url}")

    # Fetch paper IDs from collections
    if args.collection:
        try:
            collection_file = pkg_resources.resource_filename('scholtrack', f'collections/{args.collection}.txt')
            paper_ids.extend(CitationExplorerAPI.parse_paper_ids_from_file(collection_file))
        except FileNotFoundError:
            print(f"Error: Collection file {args.collection}.txt not found.")
            return

    # Fetch paper IDs from file
    if args.file:
        paper_ids.extend(CitationExplorerAPI.parse_paper_ids_from_file(args.file))

    # Fetch paper IDs from command-line input
    if args.paper_ids:
        paper_ids.extend(args.paper_ids)

    # Check if paper IDs were collected
    if not paper_ids:
        parser.error("No input provided. Use --urls, --collection, --file, or --paper-ids.")

    # Ensure an output file name if the output type is not stdout
    if args.output_type != 'stdout' and not args.output:
        print(f"Error: You must specify an output file name with --output (-o) when using output type {args.output_type}.")
        return

    print("\nScholTrack is about to start fetching citations for the provided papers.")
    print("\nNote: This process may take several minutes for large lists or papers with many citations.")

    # Start the rolling indicator in a separate thread
    stop_event = Event()
    indicator_thread = Thread(target=rolling_indicator, args=(stop_event,))
    indicator_thread.start()

    try:
        # Initialize API client
        api_client = CitationExplorerAPI(api_key=args.api_key)

        # Fetch citations
        citations = api_client.get_citations_for_papers(paper_ids, cites_at_least_n=args.cites_at_least_n)

        # Stop rolling indicator
        stop_event.set()
        indicator_thread.join()

        # Handle output
        if args.output_type == 'csv':
            CitationExporter.save_to_csv(citations, filename=args.output, sort_by=args.sort_by)
        elif args.output_type == 'json':
            CitationExporter.save_to_json(citations, filename=args.output)
        elif args.output_type == 'txt':
            CitationExporter.save_to_txt(citations, filename=args.output, sort_by=args.sort_by, show_abstract=args.show_abstract)
        elif args.output_type == 'stdout':
            CitationExporter.display_citations(citations, sort_by=args.sort_by, limit=args.display_limit, show_abstract=args.show_abstract)

        # Display additional results in the terminal if quiet mode is not enabled
        if not args.quiet:
            CitationExporter.display_citations(citations, sort_by=args.sort_by, limit=args.display_limit, show_abstract=args.show_abstract)
            sort_explanation = {
                'citations': 'citation count',
                'arxiv': 'arXiv date of appearance',
                'year': 'year of publication'
            }
            print(f"\nAll done, found {GREEN_COLOR}{len(citations)} citations{DEFAULT_COLOR}. Showing {PURPLE_COLOR}top {args.display_limit} results based on {sort_explanation[args.sort_by]}{DEFAULT_COLOR}.")
            if args.output:
                print(f"The full results are saved in {BLUE_COLOR}{args.output}{DEFAULT_COLOR}.")
                
    except Exception as e:
        stop_event.set()
        indicator_thread.join()
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    main()
