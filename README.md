# ScholTrack: Effortlessly Gather, Trace, and Analyze Citations for Academic Papers

**ScholTrack** is a Python command-line tool for fetching and exporting scholarly paper citations from Semantic Scholar. It allows users to retrieve citations for a set of paper IDs and filter, sort, and export them to various formats such as CSV, JSON, and TXT. You can specify your own paper ID collections in `.txt` files and have options for sorting and displaying the results.


## Motivation

Tracking the evolution of ideas and recent developments in a field is crucial in academic research. One effective way to do this is by following specific lines of research, particularly by keeping up with papers that cite seminal work. For instance, to stay current with neural rendering research in computer vision, you might track all papers citing foundational work like Neural Radiance Fields or 3D Gaussian Splatting. Similarly, to monitor recent advances in diffusion models, you could follow papers citing Denoising Diffusion Probabilistic Models.

ScholTrack enables you to do just that by efficiently gathering and organizing citation lists for specified papers. Additionally, it helps you explore intersections between fields, for example, by identifying papers that cite both DDPM and NeRF papers.


## Features

- Fetch citations from Semantic Scholar based on a list of paper IDs.
- **Optional API Key**: Access additional data by providing an API key. Without an API key, basic functionality is still available.
- Filter citing papers by how many source papers they reference (`cites-at-least-n` option).
- Export citations to various formats:
  - CSV
  - JSON
  - Human-readable TXT
  - Display directly in the terminal (stdout)
- Options to skip fields like abstract in the output.
- Sort citations by citation count, ArXiv ID, or year.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sergeyprokudin/scholtrack.git
    ```

2. Navigate to the repository:

    ```bash
    cd scholtrack
    ```

3. Install the package:

    ```bash
    pip install -e .
    ```

You can optionally use a **Semantic Scholar API Key** to get enhanced data. You can get one by signing up at [Semantic Scholar API](https://www.semanticscholar.org/product/api). Using an API key may increase rate limits and access to additional data.

## Getting Paper IDs

In order to use ScholTrack, you need to have the Semantic Scholar Paper ID for the papers of interest. Here’s how you can get the paper ID using the Semantic Scholar website:

1. Go to [Semantic Scholar](https://www.semanticscholar.org/).
2. Use the search bar to find the paper by entering the title or keywords.
3. Click on the appropriate search result to open the paper details page.
4. Look at the URL of the paper details page. It will be in the format:
   
   ```
   https://www.semanticscholar.org/paper/{Title}/{Paper-ID}
   ```
   
   For example, for the paper titled *"NeRF: Representing Scenes as Neural Radiance Fields"*, the URL might look like:
   
   ```
   https://www.semanticscholar.org/paper/NeRF-Mildenhall-Srinivasan/428b663772dba998f5dc6a24488fff1858a0899f
   ```
   
5. The **Paper ID** is the string at the end of the URL: `428b663772dba998f5dc6a24488fff1858a0899f`.

This **Paper ID** is what you need to use with ScholTrack to fetch citations.

## Usage

### Basic Command Structure

```bash
scholtrack --paper-ids <list-of-paper-ids> [options]
```

### Available Options

#### Input Options

- `--paper-ids <list-of-paper-ids>`: Provide a space-separated list of paper IDs to fetch citations for.
- `--file <path-to-txt-file>`: Provide a text file with paper IDs and optional comments (after `#`).

#### Output Options

- `--output-type <stdout|csv|json|txt>`: Specify the output format (default: `csv`).
- `--output <file-name>`: Specify the output file name (default: `citations.csv` for CSV).
- `--skip-abstract`: Skip the abstract field when saving to TXT or displaying in stdout.
- `--sort-by <citation_count|arxiv|year>`: Sort the results by citation count, ArXiv ID, or year (default: `citation_count`).
- `--verbose`: Display the first 10 results in the terminal (default: off).

#### Filtering Options

- `--cites-at-least-n <number>`: Only include citing papers that reference at least `n` papers from the provided list.

#### API Key

- `--api-key <your-api-key>`: Specify your Semantic Scholar API key for fetching citation data. **This is optional**; if not provided, ScholTrack will still function with basic features.

## Examples

### Example 1: Fetch Citations for Multiple Paper IDs and Export to CSV

```bash
scholtrack --paper-ids 11665dbecb17ef4d3d71b75b8666ce0e61bd43fa a57debf768b0454e60c97d16d1cf80e9b3ae8a55 --output-type csv --output my_citations.csv --api-key YOUR_API_KEY
```

This command will:
- Fetch the citations for the provided paper IDs.
- Sort the citations by the default field (citation count).
- Save the results to `my_citations.csv`.

### Example 2: Fetch and Display Citations for Paper IDs list from a File, Sorted by Year

```bash
scholtrack --file collections/nerf.txt --sort-by year --output-type stdout
```

This command will:
- Fetch citations for the paper IDs in the `collections/nerf.txt` file.
- Sort the citations by year.
- Display the results directly in the terminal (stdout).

### Example 3: Fetch Citations and Save to TXT, Skipping Abstracts

```bash
scholtrack --file collections/nerf.txt --output-type txt --output citations.txt --skip-abstract
```

This command will:
- Fetch the paper IDs from `collections/nerf.txt`.
- Skip the abstract field when saving to `citations.txt`.
- Save the results in a human-readable format to `citations.txt`.

### Example 4: Display the First 10 Citations in the Terminal

```bash
scholtrack --file collections/nerf.txt --verbose --sort-by arxiv
```

This command will:
- Fetch the paper IDs from `collections/nerf.txt`.
- Display the first 10 citations directly in the terminal.

## Folder Structure

Here’s the recommended folder structure for the repository:

```bash
scholtrack/
├── collections/               # Pre-set collections of paper IDs
│   ├── nerf.txt
├── scholtrack/
│   ├── api.py                 # Handles interactions with the Semantic Scholar API
│   ├── exporter.py            # Handles export functions (CSV, TXT, JSON, stdout)
│   ├── cli.py                 # Command-line interface definitions
├── README.md                  # This file
└── setup.py                   # Installation setup
```

### Example Paper ID Collection File: `collections/nerf.txt`

```txt
# Collection of Semantic Scholar Paper IDs related to the Neural Rendering, NeRF and 3DGS topics
428b663772dba998f5dc6a24488fff1858a0899f # Nerf: Representing scenes as neural radiance fields for view synthesis 
21336e57dc2ab9ae2171a0f6c35f7d1aba584796 # Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields
2cc1d857e86d5152ba7fe6a8355c2a0150cc280a # 3D Gaussian Splatting for Real-Time Radiance Field Rendering
```

## Development

To work on this project, you can create your own branches and implement new features or bug fixes. After making changes, you can reinstall the package in development mode:

```bash
pip install -e .
```

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

## Contributions

Feel free to contribute by creating pull requests, opening issues, or suggesting new features. Your feedback is appreciated!

## Acknowledgments

This tool uses the [Semantic Scholar API](https://www.semanticscholar.org/product/api) to retrieve scholarly citation data. Special thanks to the Semantic Scholar team for providing this service.
```
