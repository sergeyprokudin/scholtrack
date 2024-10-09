![scholtrack_demo](https://github.com/user-attachments/assets/05360671-9674-498f-87b8-682481f2ad7d)

# ScholTrack: Effortless Tracking and Analysis of Academic Citations

###  [Online Widget (No-code)](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Widget_Demo.ipynb) | [Command Line Demo](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Command_Line_Demo.ipynb)

[![Open Demo in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Command_Line_Demo.ipynb)<br> 

**ScholTrack** is a Python command-line tool designed to help researchers retrieve, organize, and export academic paper citations using [Semantic Scholar API](https://www.semanticscholar.org/product/api). Whether you want to track citations for seminal papers or survey an entire research area, ScholTrack simplifies the process of fetching, filtering, and exporting citation data in various human- and machine-readable formats, such as CSV, TXT, or JSON. It allows you to work with individual papers or collections of key works within your field.


## Installation

```bash
pip install git+https://github.com/sergeyprokudin/scholtrack.git
```

## Getting Started

The easiest way to explore ScholTrack is by [finding the Semantic Scholar Paper ID](https://github.com/sergeyprokudin/scholtrack/blob/main/README.md#finding-paper-ids) for your paper of interest and running the following command:

```bash
scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a -o 3dgs_references.csv
```

This command retrieves all papers citing [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) (Paper ID 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a), a seminal work in the novel view synthesis field. The results are saved in a CSV file named *3dgs_references.csv* and include abstracts, citation counts, arXiv links, publication venues, and more.

## No-code Demo

Alternatively, for a simple online demo, check out the provided [Colab Widget](https://colab.research.google.com/github/sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Widget_Demo.ipynb). This tool allows you to input a list of Semantic Scholar Paper IDs and retrieve the corresponding citation data, all without any coding required.

## Examples

You can try all examples directly via [a simple Colab demo](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Command_Line_Demo.ipynb).


### Example 0: Fetch All Citations for a Paper and Save to CSV

This basic command retrieves all citations and related information (such as abstract, arXiv link, citation count,  venue, etc.) for a given paper and saves it to a CSV file:

```bash
scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a -o 3dgs_references.csv
```

### Example 1: Fetch Latest Citations to a Paper, Save to TXT

You can order the output based on the paper arXiv ID to prioritize latest relevant publications:

```bash
scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a -o 3dgs_citations.txt -s arxiv -t txt
```

### Example 2: Fetch All Citations to a List of Papers

You can provide more than one Paper ID either directly in the command line:

```bash
scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a 428b663772dba998f5dc6a24488fff1858a0899f -o nvs_citations.txt
```

or by providing a TXT file with the Paper ID list:

```bash
scholtrack -f nvs.txt -o nvs_citations.txt
```

Here, `nvs.txt` is the following file which contains recent seminal works in the novel view synthesis (NVS) field:

```txt
# Collection of Semantic Scholar Paper IDs related to Neural Rendering, NeRF, and 3DGS
428b663772dba998f5dc6a24488fff1858a0899f # Nerf: Representing scenes as neural radiance fields for view synthesis 
21336e57dc2ab9ae2171a0f6c35f7d1aba584796 # Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields
2cc1d857e86d5152ba7fe6a8355c2a0150cc280a # 3D Gaussian Splatting for Real-Time Radiance Field Rendering
```

You can create custom paper collections to track daily progress in your field of interest or conduct comprehensive surveys.

**Note**: Retrieving results for papers with thousands of citations or long citation lists may take a few minutes. Additionally, the current limit for citations that can be retrieved from the Semantic Scholar API without an API key is 10,000 per paper.


### Example 3: Finding Papers at the Intersection of Fields

You can perform a more targeted search to find papers that cite multiple works from a given list. This is useful for identifying papers that lie at the intersection of different research fields. For example, the following command finds all papers that cite both [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) and the seminal work *["SMPL: A Skinned Multi-Person Linear Model"](https://smpl.is.tue.mpg.de/)* on digital humans, offering a comprehensive view of how 3DGS techniques are applied in digital avatar modeling:

```bash
scholtrack -o avatar_3dgs.csv -n 2 -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a 32d3048a4fe4becc7c4638afd05f2354b631cfca
```

Here, `-n 2` indicates that only papers citing at least two works from the list are of interest.


### Example 4: Using Pre-built Paper Collections

You can also explore pre-packaged lists of papers included in the repository. Currently, we offer the "Novel View Synthesis" (nvs) collection, which tracks papers related to this topic, including works such as NeRF, 3DGS, and [DreamFusion](https://dreamfusion3d.github.io/). To retrieve the corresponding citations, run:

```bash
scholtrack -c nvs -o novel_view_synthesis_works.csv -s arxiv
```

In this example, `-s arxiv` sorts the results by the arXiv date of appearance.

## Finding Paper IDs

ScholTrack uses **Semantic Scholar Paper IDs** to retrieve citations. To find a Paper ID:

1. Go to [Semantic Scholar](https://www.semanticscholar.org/).
2. Search for the paper.
3. Click on the paper in the results.
4. The Paper ID is the string after the last slash in the URL, e.g., for 3D Gaussian Splatting:

   ```
   https://www.semanticscholar.org/paper/3D-Gaussian-Splatting-for-Real-Time-Radiance-Field-Kerbl-Kopanas/2cc1d857e86d5152ba7fe6a8355c2a0150cc280a
   ```

   The Paper ID is `2cc1d857e86d5152ba7fe6a8355c2a0150cc280a`.

Use this ID in ScholTrack to retrieve citations. Alternatively, you can provide the Semantic Scholar URL directly as input:

```
scholtrack -u https://www.semanticscholar.org/paper/3D-Gaussian-Splatting-for-Real-Time-Radiance-Field-Kerbl-Kopanas/2cc1d857e86d5152ba7fe6a8355c2a0150cc280a -o 3dgs_references.csv
```

## Python API Usage

```python
from scholtrack.api import CitationExplorerAPI
from scholtrack.exporter import CitationExporter

# Initialize the API client (API key is optional)
api = CitationExplorerAPI()

# Fetch citations for a paper
paper_ids = ["395bfdae59f1a5fde16213cade43d2587e4565df",
             "8ba2c82fe675ede1d5c12fc4f97cf8ca3ebf1ca3"]

citations = api.get_citations_for_papers(paper_ids)

# Save citations to a CSV file
CitationExporter.save_to_csv(citations, filename="citations.csv")
```

This will save the retrieved citation data for the specified Paper IDs to a CSV file.

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for more information.

## Contributions

Contributions are welcome. Feel free to submit pull requests, report issues, or suggest new features.

## Acknowledgments

This tool leverages the [Semantic Scholar API](https://www.semanticscholar.org/product/api) to fetch scholarly citation data. Special thanks to the Semantic Scholar team for providing this valuable service.
