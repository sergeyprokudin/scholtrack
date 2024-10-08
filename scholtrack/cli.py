import argparse
import os
import sys
import time
from pathlib import Path
from threading import Thread
from scholtrack.api import CitationExplorerAPI
from scholtrack.exporter import CitationExporter
import re

# Define the path to the collections folder in the root directory of the repository
ROOT_COLLECTIONS_DIR = Path(__file__).resolve().parent.parent / 'collections'

def rolling_indicator():
    """A simple rolling progress indicator to show the process is ongoing."""
    while True:
        for symbol in "|/-\\":
            sys.stdout.write(f"\rProcessing... {symbol}")
            sys.stdout.flush()
            time.sleep(0.2)

def print_header():
    """Print a nice header with ******* and author information."""
    print("\n" + "*" * 70)
    print("*" * 8 + "    ScholTrack: Fetch Citations for Academic Papers   " + "*" * 8)
    print("*" * 70)
    print("Author: Sergey Prokudin")
    print("Email: sergey.prokudin@gmail.com")
    print("Date: 2024")
    print("*" * 70 + "\n")

    
def extract_paper_id(url: str) -> str:
    """
    Extract the paper ID from a Semantic Scholar URL.

    Args:
        url (str): The Semantic Scholar URL to extract the paper ID from.

    Returns:
        str: The extracted paper ID, or an empty string if not found.
    """
    # Define a regular expression to match the Paper ID pattern from the URL
    pattern = r"semanticscholar\.org/paper/.+?/([a-f0-9]{40})"
    
    # Try to find the paper ID using the regular expression
    match = re.search(pattern, url)
    
    if match:
        # Return the matched Paper ID
        return match.group(1)
    else:
        # Return an empty string if no match is found
        return ""

    
def main():
    # Print the header
    print_header()

    parser = argparse.ArgumentParser(
        description='ScholTrack Command-Line Interface: Fetch Citations for Papers via Semantic Scholar API',
        epilog='''Usage examples:

        1. Fetch citations for multiple paper IDs and export to CSV:
            scholtrack -p 11665dbecb17ef4d3d71b75b8666ce0e61bd43fa a57debf768b0454e60c97d16d1cf80e9b3ae8a55 -o my_citations.csv -t csv

        2. Fetch and display citations for Paper IDs from a file, sorted by year:
            scholtrack -f collections/nerf.txt -s year -t stdout

        3. Fetch citations for papers in the "nerf" collection, but only display those citing at least 2 papers from the list:
            scholtrack -c nerf -n 2 -t stdout

        4. Fetch citations and save to TXT, sorted by ArXiv ID, and skipping abstracts:
            scholtrack -f collections/nerf.txt -t txt -o citations.txt --skip-abstract -s arxiv

        5. Fetch and display citations from URLs, exporting results to CSV:
            scholtrack --urls https://www.semanticscholar.org/paper/LGM%3A-Large-Multi-View-Gaussian-Model-for-3D-Content-Tang-Chen/11665dbecb17ef4d3d71b75b8666ce0e61bd43fa -o my_citations.csv -t csv

        6. Display the first 10 citations in the terminal, including abstracts:
            scholtrack -f collections/nerf.txt -v --show-abstract
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Main command to get citations
    parser.add_argument('-p', '--paper-ids', nargs='+', help='List of paper IDs to get citations for')
    parser.add_argument('-u', '--urls', nargs='+', help='List of Semantic Scholar URLs to get paper IDs from')
    parser.add_argument('-f', '--file', help='Path to the text file with paper IDs and optional comments')
    parser.add_argument('-c', '--collection', help='Name of the collection (automatically looks in collections/ folder in the repository root)')
    parser.add_argument('-n', '--cites-at-least-n', type=int, default=0, help='Minimum number of papers a citing paper must reference from the provided list')
    parser.add_argument('-t', '--output-type', choices=['stdout', 'csv', 'json', 'txt'], default='csv', help='Specify the output format: stdout, csv, json, or txt')
    parser.add_argument('-o', '--output', help='Output file name for csv, json, or txt formats')
    parser.add_argument('-s', '--sort-by', choices=['citations', 'arxiv', 'year'], default='citations', help='Specify the field by which to sort the citations')
    parser.add_argument('--show-abstract', action='store_true', help='Show the abstract field when saving or displaying results')
    parser.add_argument('-q', '--quiet', action='store_true', help='Omit displaying first N citations in the command line')
    parser.add_argument('-k', '--api-key', help='Semantic Scholar API Key (optional)')
    parser.add_argument('-l', '--display-limit', type=int, default=5, help='Maximum number of found papers to show in terminal')

    args = parser.parse_args()

    # Check if any input is provided (either --collection, --file, --paper-ids, or --urls)
    paper_ids = []

    if args.urls:
        print(f"Fetching paper IDs from provided URLs.")
        for url in args.urls:
            paper_id = extract_paper_id(url)
            if paper_id:
                paper_ids.append(paper_id)
            else:
                print(f"Warning: Unable to extract paper ID from URL {url}")

    if args.collection:
        print(f"Fetching citations for papers from the collection: {args.collection}.")
        collection_file = ROOT_COLLECTIONS_DIR / f'{args.collection}.txt'
        if collection_file.exists():
            paper_ids.extend(CitationExplorerAPI.parse_paper_ids_from_file(collection_file))
        else:
            print(f"Error: Collection file {args.collection}.txt not found in the collections/ folder.")
            return
    elif args.file:
        print(f"Fetching citations for papers listed in the file: {args.file}.")
        paper_ids.extend(CitationExplorerAPI.parse_paper_ids_from_file(args.file))
    elif args.paper_ids:
        print(f"Fetching citations for the specified paper IDs: {', '.join(args.paper_ids)}.")
        paper_ids.extend(args.paper_ids)

    if not paper_ids:
        # If no input is provided, display an error and usage example
        parser.error(
            "No input provided. Please specify at least one of the following options: "
            "--urls (-u), --collection (-c), --file (-f), or --paper-ids (-p).\n\n"
            "Example:\n"
            "    scholtrack -u https://www.semanticscholar.org/paper/11665dbecb17ef4d3d71b75b8666ce0e61bd43fa -o citations.csv -t csv"
        )

    print("\nScholTrack is about to start fetching citations for the provided papers.")
    print("\nNote: This process may take several minutes for papers with many citations or larger lists.")

    # Ensure an output file name is provided if output type is not stdout
    if args.output_type != 'stdout' and not args.output:
        print(f"Error: You must specify an output file name with --output (-o) when using output type {args.output_type}.")
        return

    # Start the rolling indicator in a separate thread
    indicator_thread = Thread(target=rolling_indicator)
    indicator_thread.daemon = True  # This makes sure the thread will exit when the main program exits
    indicator_thread.start()

    # Initialize the API client with or without the API key
    api_client = CitationExplorerAPI(api_key=args.api_key)

    # Fetch citations, ensuring uniqueness and applying the cites_at_least_n filter
    citations = api_client.get_citations_for_papers(paper_ids, cites_at_least_n=args.cites_at_least_n)
    n_citations = len(citations)

    # Stop the rolling indicator by completing the main process
    sys.stdout.write("\rProcessing complete.        \n")

    # Handle output type with sorting and abstract skip option
    if args.output_type == 'csv':
        CitationExporter.save_to_csv(citations, filename=args.output, sort_by=args.sort_by)
        print(f"%d citations saved to {args.output}" % n_citations)
    elif args.output_type == 'json':
        CitationExporter.save_to_json(citations, filename=args.output)
        print(f"%d citations saved to {args.output}" % n_citations)
    elif args.output_type == 'txt':
        CitationExporter.save_to_txt(citations, filename=args.output, sort_by=args.sort_by, show_abstract=args.show_abstract)
        print(f"%d citations saved to {args.output}" % n_citations)
    elif args.output_type == 'stdout':
        CitationExporter.display_citations(citations, sort_by=args.sort_by, limit=args.display_limit, show_abstract=args.show_abstract)

    # Display first N results in the command line if quiet mode is not enabled
    if not args.quiet:
        CitationExporter.display_citations(citations, sort_by=args.sort_by, limit=args.display_limit, show_abstract=args.show_abstract)
        if args.sort_by == 'year' or args.sort_by == 'arxiv':
            sort_type = 'latest'
        else:
            sort_type = 'most cited'
        print(f"\nAll done, found {n_citations} citations. Showing {args.display_limit} {sort_type} works above, please see the {args.output} for the full list.")

if __name__ == '__main__':
    main()
