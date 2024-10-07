import argparse
import os
from scholtrack.api import CitationExplorerAPI
from scholtrack.exporter import CitationExporter

def main():
    parser = argparse.ArgumentParser(
        description='ScholTrack Command-Line Interface: Fetch Citations for Papers via Semantic Scholar API',
        epilog='''Usage examples:

        1. Fetch citations for multiple paper IDs and export to CSV:
            scholtrack --paper-ids 11665dbecb17ef4d3d71b75b8666ce0e61bd43fa a57debf768b0454e60c97d16d1cf80e9b3ae8a55 --output-type csv --output my_citations.csv

        2. Fetch and display citations for Paper IDs from a file, sorted by year:
            scholtrack --file collections/nerf.txt --sort-by year --output-type stdout

        3. Fetch citations and save to TXT, skipping abstracts:
            scholtrack --file collections/nerf.txt --output-type txt --output citations.txt --skip-abstract

        4. Display the first 10 citations in the terminal:
            scholtrack --file collections/nerf.txt --verbose

        Note: To get Semantic Scholar Paper IDs, visit https://www.semanticscholar.org, search for the paper, and extract the ID from the URL (see README for detailed instructions). E.g., for the paper https://www.semanticscholar.org/paper/NeRF-Mildenhall-Srinivasan/428b663772dba998f5dc6a24488fff1858a0899f, its Paper ID is 428b663772dba998f5dc6a24488fff1858a0899f''',
        formatter_class=argparse.RawTextHelpFormatter  # This ensures the multi-line format is preserved
    )

    # Main command to get citations
    parser.add_argument('--paper-ids', nargs='+', help='List of paper IDs to get citations for')
    parser.add_argument('--file', help='Path to the text file with paper IDs and optional comments')
    parser.add_argument('--cites-at-least-n', type=int, default=0, help='Minimum number of papers a citing paper must reference from the provided list')
    parser.add_argument('--output-type', choices=['stdout', 'csv', 'json', 'txt'], default='csv', help='Specify the output format: stdout, csv, json, or txt')
    parser.add_argument('--output', default='citations.csv', help='Output file name for csv, json, or txt formats')
    parser.add_argument('--sort-by', choices=['citation_count', 'arxiv', 'year'], default='citation_count', help='Specify the field by which to sort the citations')
    parser.add_argument('--skip-abstract', action='store_true', help='Skip the abstract field when saving or displaying results')
    parser.add_argument('--verbose', action='store_true', help='Display first 10 citations in the command line')
    parser.add_argument('--api-key', help='Semantic Scholar API Key (optional)')

    args = parser.parse_args()

    # Initialize the API client with or without the API key
    api_client = CitationExplorerAPI(api_key=args.api_key)

    # Paper IDs can come from --paper-ids or --file
    paper_ids = []

    if args.file:
        # Parse paper IDs from the provided file
        paper_ids = api_client.parse_paper_ids_from_file(args.file)
    elif args.paper_ids:
        # Use paper IDs from the command line input
        paper_ids = args.paper_ids

    if not paper_ids:
        print("Error: No paper IDs provided. Please use --paper-ids or --file. See README for instructions on how to obtain paper IDs.")
        return

    # Fetch citations, ensuring uniqueness and applying the cites_at_least_n filter
    citations = api_client.get_citations_for_papers(paper_ids, cites_at_least_n=args.cites_at_least_n)

    # Handle output type with sorting and abstract skip option
    if args.output_type == 'csv':
        CitationExporter.save_to_csv(citations, filename=args.output, sort_by=args.sort_by)
        print(f"Citations saved to {args.output}")
    elif args.output_type == 'json':
        CitationExporter.save_to_json(citations, filename=args.output)
        print(f"Citations saved to {args.output}")
    elif args.output_type == 'txt':
        CitationExporter.save_to_txt(citations, filename=args.output, sort_by=args.sort_by, skip_abstract=args.skip_abstract)
        print(f"Citations saved to {args.output}")
    elif args.output_type == 'stdout':
        CitationExporter.display_citations(citations, sort_by=args.sort_by, skip_abstract=args.skip_abstract)

    # Display first 10 results in the command line if verbose mode is enabled
    if args.verbose:
        print("\nShowing first 10 citations:\n")
        CitationExporter.display_citations(citations, sort_by=args.sort_by, limit=10, skip_abstract=args.skip_abstract)

if __name__ == '__main__':
    main()
