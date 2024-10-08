![scholtrack](https://github.com/user-attachments/assets/368377a3-c43b-4d59-a656-0f70f9d3f329)

# ScholTrack: Track, Collect, and Analyze Academic Paper Citations

[![Open Demo in Colab (Widget, No Code)](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Widget_Demo.ipynb)<br> 


**ScholTrack** is a Python command-line tool that helps researchers retrieve, organize, and export scholarly paper citations from [Semantic Scholar](https://www.semanticscholar.org/). Whether you need to track citations for specific papers or monitor the evolution of ideas across research fields, ScholTrack makes it easy to fetch, filter, and export citation data. You can work with individual papers or collections of key papers in your field.

## Motivation

Tracking the evolution of ideas and staying up to date with developments in your research field is crucial for academic success. Often, this involves keeping an eye on papers that cite certain **seminal works**. For example, to follow the latest progress in neural rendering research, you might track papers citing foundational works like Neural Radiance Fields (NeRF) or 3D Gaussian Splatting. Similarly, to stay on top of advances in diffusion models, you could follow papers citing Denoising Diffusion Probabilistic Models (DDPM).

ScholTrack enables you to do this seamlessly by _**gathering and organizing citation lists for specified papers**_. This can be achieved via a single command. Furthermore, it allows you to explore intersections between fields, for example, by identifying papers that cite multiple seminal papers across different domains.


## Getting Started 

The simplest way to explore ScholTrack is by running the following command:

```bash
pip install git+https://github.com/sergeyprokudin/scholtrack.git
scholtrack -c nerf -o nerf_citations.csv
```

This command will retrieve all papers that cite key works in the Neural Rendering field, including NeRF (Neural Radiance Fields), 3D Gaussian Splatting, and DreamFusion, from the Semantic Scholar database. The results will be saved in a CSV file called nerf_citations.csv

By using the pre-configured collection named nerf, you can quickly gather citations for multiple influential papers in the field with just one command. This is ideal for tracking major developments in a research area without having to specify individual paper IDs.

To see the contents of the nerf collection or modify it, check the collections/nerf.txt file, which contains the Semantic Scholar Paper IDs for these papers. You can also create your own collections by adding new .txt files in the collections/ folder.

## Tracking Paper Lists

Instead of tracking citations for a single paper, ScholTrack allows you to define and manage **collections** of paper IDs. These collections can represent the most influential works in a specific research area. By using collections, you can:
- Fetch all citations to multiple seminal works in one go.
- Share and extend paper collections with collaborators.
- Monitor broader developments in your field by tracking a group of influential papers.

Collections are stored as simple `.txt` files, making them easy to create, update, and share.

## Features

- Fetch citations from Semantic Scholar based on one or more paper IDs.
- Define and track **collections** of papers.
- Filter citing papers by how many source papers they reference (`--cites-at-least-n`).
- Export citations to various formats:
  - CSV
  - JSON
  - Human-readable TXT
  - Display directly in the terminal (stdout)
- Skip fields like abstract in the output (`--skip-abstract`).
- Sort citations by citation count, ArXiv ID, or year (`--sort-by`).

## Installation

To get started, clone and install the repository:

```bash
git clone https://github.com/sergeyprokudin/scholtrack.git
cd scholtrack
pip install -e .
```

For enhanced functionality, you can use a **Semantic Scholar API Key**. This provides access to additional data and may improve rate limits. Get your API key from [Semantic Scholar API](https://www.semanticscholar.org/product/api).

## Getting Paper IDs

ScholTrack uses **Semantic Scholar Paper IDs** to retrieve citations. You can find these IDs using the Semantic Scholar website:

1. Visit [Semantic Scholar](https://www.semanticscholar.org/).
2. Search for a paper by its title or keywords.
3. Click on the paper in the search results.
4. Look at the URL in your browser's address bar. It will be in the format:

   ```
   https://www.semanticscholar.org/paper/{Title}/{Paper-ID}
   ```

   Example for *"NeRF: Representing Scenes as Neural Radiance Fields"*:

   ```
   https://www.semanticscholar.org/paper/NeRF-Mildenhall-Srinivasan/428b663772dba998f5dc6a24488fff1858a0899f
   ```

5. The **Paper ID** is the string after the last slash: `428b663772dba998f5dc6a24488fff1858a0899f`.

Use this Paper ID in ScholTrack to fetch citations.

## Usage

### Basic Command Structure

```bash
scholtrack --paper-ids <list-of-paper-ids> [options]
```

### Available Options

#### Input Options

- `--paper-ids <list-of-paper-ids>`: Space-separated list of paper IDs to fetch citations for.
- `--file <path-to-txt-file>`: Path to a text file with paper IDs (one per line).
- `--collection <collection-name>`: Use a collection of paper IDs from the `collections/` folder.

#### Output Options

- `--output-type <stdout|csv|json|txt>`: Output format (default: `csv`).
- `--output <file-name>`: Specify the output file name (default: `citations.csv`).
- `--skip-abstract`: Skip the abstract field in TXT or terminal output.
- `--sort-by <citations|arxiv|year>`: Sort results by citation count, ArXiv ID, or year (default: `citations`).
- `--show-abstract`: Include the abstract field in the output.
- `--quiet`: Suppress terminal output of citations.

#### Filtering Options

- `--cites-at-least-n <number>`: Include only papers that reference at least `n` of the input papers.

#### Other Options

- `--display-limit <number>`: Maximum number of citations to display in the terminal (default: 5).

#### API Key

- `--api-key <your-api-key>`: Specify your Semantic Scholar API key for fetching citation data. **Optional** — ScholTrack will work without it but may have lower rate limits.

## Examples

You can try all examples directly in the [simple Colab demo](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Command_Line_Demo.ipynb).

### Example 1: Fetch Citations for Multiple Paper IDs and Export to CSV

```bash
scholtrack --paper-ids 11665dbecb17ef4d3d71b75b8666ce0e61bd43fa --output-type csv --output my_citations.csv
```

This command fetches citations for the provided paper IDs, sorts them by citation count, and saves the results to `my_citations.csv`.

### Example 2: Fetch and Display Citations from a File, Sorted by ArXiv ID

```bash
scholtrack --file collections/nerf.txt --sort-by arxiv --output-type stdout
```

This command fetches citations for papers listed in `collections/nerf.txt`, sorts them by ArXiv ID, and displays the results in the terminal.

### Example 3: Fetch Citations and Save to TXT, Skipping Abstracts

```bash
scholtrack --file collections/nerf.txt --output-type txt --output citations.txt --skip-abstract
```

This command fetches citations, skips the abstract field, and saves the results in a human-readable format to `citations.txt`.

### Example 4: Fetch Citations for Papers in the "nerf" Collection, Displaying Papers that Cite at Least 2 Works

```bash
scholtrack -c nerf -o nerf_citations.csv -n 2 -t csv
```

This command fetches citations for the "nerf" collection and only includes papers that cite at least two of the works from the collection.

### Example Paper ID Collection File: `collections/nerf.txt`

```txt
# Collection of Semantic Scholar Paper IDs related to Neural Rendering, NeRF, and 3DGS
428b663772dba998f5dc6a24488fff1858a0899f # Nerf: Representing scenes as neural radiance fields for view synthesis 
21336e57dc2ab9ae2171a0f6c35f7d1aba584796 # Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields
2cc1d857e86d5152ba7fe6a8355c2a0150cc280a # 3D Gaussian Splatting for Real-Time Radiance Field Rendering
```

## Development

To contribute to ScholTrack, feel free to fork the repository, implement new features or bug fixes, and submit pull requests. After making changes, you can reinstall the package in development mode:

```bash
pip install -e .
```

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for more information.

## Contributions

Contributions are welcome! Feel free to submit pull requests, report issues, or suggest new features.

## Acknowledgments

This tool leverages the [Semantic Scholar API](https://www.semanticscholar.org/product/api) to fetch scholarly citation data. Special thanks to the Semantic Scholar team for providing this valuable service.