# AcademicBibtexGraph

This code uses the Microsoft Academics Research API to fetch references and citations based on a bibtex library and build a dependency graph. It solely tries to get the references by name. To use it you must register [here](https://msr-apis.portal.azure-api.net/products) for a key. It could be used to check how references found during literature search are related or to get new references via forward or backward search.

**Warning: Currently Microsoft only grants about 10000 free transactions over the API per month. Especially using forward or backward search can consume this very quickly.**

***Example 1: Illustration of internal dependencies***  
*Created with GraphViz (used by visualizeGraph.py), layout hierarchical*
![Illustration1](https://github.com/alexanderadgk/AcademicBibtexGraph/blob/main/examples/illustration_big_40.svg)  


***Example 2:Illustration of forward and backwards search of 4 related papers***  
*Created with Gephi from the produced graphml-Flle, colors label the source (orange: input,blue: backward search,green: forward search)*
![Illustration2](https://github.com/alexanderadgk/AcademicBibtexGraph/blob/main/examples/illustration_small_4.svg)  


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
The first command creates a graphml file, while the second one makes a visualization as PDF. You can also visualize the graphml-file with a tool like Gephi.

### createGraph.py

`python creatGraph.py --help`
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

Usually this script will make 1 query per item of your bibtex-file where it will get the attributes Id, Ti, DN, RId (Identification number, Title, Original Paper Title, Reference Ids). If you activate **--backward** it will additionally perform a backward search, meaning that for all RIds it got in the first run it will make another query to receive the names and references of those papers (to get also the connections between the referenced papers). This means 1 query per reference cited by your input papers (this can quickly blow up to e.g. 50x50 = 2500 queries if you pass 50 papers that cite on average 50 papers). Further if you activate **--forward** it will make query all Ids of papers that have your input papers as RId (This takes again 1 query per input paper). Than it will get the names and references of those papers, which will take 1 query per citation. Note that this can blow up even quicker as some major papers can have a few thousand citations.


### visualizeGraph.py
`python visualizeGraph.py --help`
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
