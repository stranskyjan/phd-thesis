## Mesoscale Discrete Element Model for Concrete and Its Combination with FEM
The source code of my Ph.D. thesis (including also source code to all the results and graphs).

The thesis was created on [Ubuntu 16.04 LTS](http://www.ubuntu.com/) system using pdfLaTeX.
Some of the figures were created using [RaphaëlPy project](http://github.com/stranskyjan/raphaelpy).
Results of chapter 5 were obtained using [dem-fem-coupling project](http://github.com/stranskyjan/dem-fem-coupling)
Other results were obtained using [discrete element code YADE](http://yade-dem.org) and [finite element code OOFEM](http://www.oofem.org).

Other prerequisites:
- [python](http://www.python.org/)
- [gnuplot](http://www.gnuplot.info/)
- [rsvg-convert](http://librsvg.sourceforge.net/) (to convert SVG figures to PDF format)
- [minieigen](https://github.com/eudoxos/minieigen) python module

To compile all the content, run [compile.sh script](compile.sh).

#### What is here
- [text](text) ... source code for text part (actual thesis, thesis statement, poster, CD cover)
- [codes](codes) ... scripts generating [results](results) and diff files for used OOFEM and YADE versions
- [results](results) ... output of [scripts](codes/scripts)
- [pdfs](pdfs) ... contains resulting PDF files

#### TODO
- cleanup and comments in scripts
