# AcademicBibtexGraph

<img src="https://github.com/alexanderadgk/AcademicBibtexGraph/blob/main/examples/readme_examples.png" alt="Picture of Example" width="685" height="730">

This code uses the Microsoft Academics Research API to fetch references and citations based on a bibtex library and build a dependency graph. It solely tries to get the references by name. To use it you must register [here](https://msr-apis.portal.azure-api.net/products) for a key.

## Installation

First clone the repository and cd to the directory. Then:
```
conda env create -f install\environment.yml
conda activate bibGraphEnv
dot -c
```
Of course you can also install the needed packages to your root environment if you wish to do so.

## Basic Usage
Put your libary in the folder with the python files.
```
python createGraph --file=inputLibary.bib --key=<YOURKEY> --output=output\firstGraph.graphml
python visualizeGraph --file=output\firstGraph.graphml --output=output\firstPlot.pdf
```
The first command creates a graphml file, while the second one makes a visualization as PDF. You can also visualize the graphml-File with a tool like Gephi.

### createGraph.py

Output of --help:
```
usage: createGraph.py [-h] --file FILE --key KEY [--forward] [--backward] [--output OUTPUT] [--silent]

optional arguments:
  -h, --help       show this help message and exit
  --file FILE      Bibtex Input File
  --key KEY        Microsoft Academics API key
  --forward        Perform forward search
  --backward       Perform backwards search
  --output OUTPUT  You can specify the output file name
  --silent         Execute without asking questions...

```

### visualizeGraph.py
Output of --help:
```
usage: visualizeGraph.py [-h] --file FILE [--output OUTPUT] [--brightedges] [--omitforward] [--omitbackward]

optional arguments:
  -h, --help       show this help message and exit
  --file FILE      GraphML Input File
  --output OUTPUT  You can specify the output file name
  --brightedges    Hide the edges
  --omitforward    Do not plot the forward search
  --omitbackward   Do not plot the backward search
  --size SIZE      Size of the figure e.g. --size=180,120
````
