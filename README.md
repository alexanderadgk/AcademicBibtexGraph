# AcademicBibtexGraph

> Picture

This code uses the Microsoft Academics Research API to fetch references and citations based on a bibtex library and build a dependency graph. It solely tries to get the references by name.

##Installation

First clone the repository and cd to the directory. Then:
```
conda env create -f install\environment.yml
conda activate bibGraphEnv
dot -c
```

##Usage
```
python createGraph --file=inputLibary.bib --key=<YOURKEY> --output=output\firstGraph.graphml
python visualizeGraph --file=output\firstGraph.graphml --output=output\firstPlot.pdf
```

###createGraph.py

###visualizeGraph.py