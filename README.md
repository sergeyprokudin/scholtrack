![scholtrack](https://github.com/user-attachments/assets/368377a3-c43b-4d59-a656-0f70f9d3f329)

# ScholTrack: Track, Collect, and Analyze Academic Citations

[![Open Demo in Colab (Widget, No Code)](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Widget_Demo.ipynb)<br> 

**ScholTrack** is a Python command-line tool designed to help researchers retrieve, organize, and export academic paper citations using [Semantic Scholar API](https://www.semanticscholar.org/product/api). Whether you want to track citations for seminal papers or survey an entire research area, ScholTrack simplifies the process of fetching, filtering, and exporting citation data in various human- and machine-readable formats, such as CSV, TXT, or JSON. It allows you to work with individual papers or collections of key works within your field.


## Installation

```bash
pip install git+https://github.com/sergeyprokudin/scholtrack.git
```

## Getting Started

The simplest way to explore ScholTrack is by running the following command:

```bash
scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a -o 3dgs_references.csv
```

This command retrieves all papers citing [3D Gaussian Splatting](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/), a recent seminal work in the novel view synthesis field. The results are saved in a CSV file called *3dgs_references.csv* and include paper abstracts, citation counts, links to arXiv, publishing venues, and more.

## Examples

You can try all examples directly via [a simple Colab demo](https://colab.research.google.com/github//sergeyprokudin/scholtrack/blob/main/colab/ScholTrack_Command_Line_Demo.ipynb).


### Example 1: Fetch Latest Citations to a Paper (Ordered by arXiv ID), Save to TXT

You can order the output based on the paper arXiv ID to get the latest relevant publications:

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

You can perform a more focused search to find papers that cite more than one work from a list. This is useful for identifying papers that lie at the intersection of different fields. For instance, the following search finds all papers that cite both 3D Gaussian Splatting (3DGS) and the seminal work *["SMPL: A Skinned Multi-Person Linear Model"](https://smpl.is.tue.mpg.de/)* on digital humans:

```bash
scholtrack -p 2cc1d857e86d5152ba7fe6a8355c2a0150cc280a 32d3048a4fe4becc7c4638afd05f2354b631cfca -o 3dgs_humans.csv -n 2
```

Here, `-n 2` specifies that we are only interested in works that cite at least two papers from the list.

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

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for more information.

## Contributions

Contributions are welcome. Feel free to submit pull requests, report issues, or suggest new features.

## Acknowledgments

This tool leverages the [Semantic Scholar API](https://www.semanticscholar.org/product/api) to fetch scholarly citation data. Special thanks to the Semantic Scholar team for providing this valuable service.