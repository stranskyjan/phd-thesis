%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% LaTeX template for PhD thesis typesetting
%
% (C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\message{*******************************************************************}
\message{LaTeX template for PhD thesis typesetting}
\message{(C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)}
\message{*******************************************************************}

\NeedsTeXFormat{LaTeX2e}%[1996/12/01]
\ProvidesClass{phdthesis}[2018/01/31 PhD thesis class]

\newcommand{\showframe}{false}
\DeclareOption{showframe}{\renewcommand{\showframe}{true}}
\ProcessOptions\relax

\LoadClass[12pt,twoside,openright]{report}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% base packages
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage[%
	inner=1in,%
	outer=1in,%
	top=1in,%
	bottom=1in,%
	a4paper,%
	showframe=\showframe%
]{geometry}
\RequirePackage{cmap} % pdf file search
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}

\RequirePackage[main=english,czech]{babel}
\RequirePackage[unicode]{hyperref}
\RequirePackage{hyphenat}
\RequirePackage{url}

\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BiBTeX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage[style=numeric,giveninits=true,backend=biber,maxnames=99]{biblatex}
\DeclareFieldFormat[article]{title}{#1}
\renewbibmacro{in:}{\ifentrytype{article}{}{\printtext{\bibstring{in}\intitlepunct}}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% titlesec
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{titlesec}
\titleformat{\part}[display]{\centering\normalfont\Huge\sf\bfseries}{Part \thepart.}{1em}{\thispagestyle{empty}}
\titleformat{name=\chapter}{\normalfont\LARGE\bfseries\filinner}{}{0em}{\thispagestyle{main}\thechapter\hspace{.6em}}
\titleformat{name=\chapter,numberless}{\normalfont\LARGE\bfseries\filinner}{}{0em}{\thispagestyle{main}}
\titleformat{\section}{\normalfont\Large\bfseries}{}{0em}{\thesection\hspace{.6em}}
\titleformat{\subsection}{\normalfont\large\bfseries}{}{0em}{\thesubsection\hspace{.6em}}
\setcounter{secnumdepth}{3}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries}{}{0em}{\thesubsubsection\hspace{.6em}}
\titleformat{\paragraph}{\normalfont\normalsize\bfseries}{}{0em}{}
\titlespacing*{\chapter}{0pt}{*0}{*3}
\newcommand{\chapterNonumber}[1]{%
	\phantomsection%
	\addcontentsline{toc}{chapter}{#1}%
	\chapter*{#1}%
	\chaptermark{#1}%
}

\let\partOrig\part
\let\myparttitle\empty
\let\mytitleintro\empty
\renewcommand{\part}[1]{
	\cleardoublepageempty
	\pagestyle{empty}
	\doubleblankpage%
	\partOrig{#1}%
	\pagestyle{main}%
	\renewcommand{\myparttitle}{#1}% \parttitle does not work with titleps
	\renewcommand{\mytitleintro}{\empty}
}

\let\chapterOrig\chapter
\newcommand{\mychapter}[2][]{%
	\chapterOrig[#1]{#2}%
	\renewcommand{\mytitleintro}{1}%
}
\newcommand{\mychapterStar}[1]{%
	\chapterOrig*{#1}%
}
\makeatletter
\renewcommand{\chapter}{%
	\@ifstar{\mychapterStar}{\@dblarg\mychapter}%
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% titleps
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{titleps}
\newpagestyle{main}{%
	\setheadrule{.7pt}%
	\sethead*{%
		\sc%
		\ifthenelse{\equal{\mypagestyle}{nonumber}}%
			{}%
			{\ifthenelse{\equal{\mytitleintro}{\empty}}%
				{\myparttitle}%
				{\thechapter\ \ \chaptertitle}%
			}
		}%
		{}%
		{\thepage}%
}
\newcommand{\headingstyle}{normal}
\newcommand{\setheadingstyle}[1]{%
	\renewcommand{\headingstyle}[2]{##1}%
}
\newcommand{\mypagestyle}{normal}
\newcommand{\headingNormal}{\edef\mypagestyle{normal}}
\newcommand{\headingNonumber}{\edef\mypagestyle{nonumber}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% fonts
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand{\familydefault}{\sfdefault}
\RequirePackage[scaled]{helvet}
\RequirePackage[helvet]{sfmath}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% other packages
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage[%
	labelsep=colon,%
	justification=centering,%
	margin=1cm,%
	figureposition=below,%
	tableposition=above%
]{caption}

\RequirePackage{graphicx}
\RequirePackage{xstring}
\RequirePackage{xcolor}
\definecolor{colorCTU}{RGB}{0,101,189}

\RequirePackage{enumitem}
\setitemize{itemsep=0em,topsep=.5em}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% commands
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\makeatletter
\newcommand{\mydotfill}[1]{\leavevmode \cleaders \hb@xt@ #1{\hss .\hss }\hfill \kern \z@}
\makeatother

\newcommand{\cleardoublepageempty}{%
	\newpage%
	\pagestyle{empty}%
	\cleardoublepage%
	\pagestyle{main}%
}
\newcommand{\blankpage}{\newpage\null\thispagestyle{empty}\newpage}
\newcommand{\doubleblankpage}{\blankpage\blankpage}

\pdfsuppresswarningpagegroup=1

\makeatletter
\renewcommand{\fps@figure}{!htbp}
\renewcommand{\fps@table}{!htbp}
\makeatother

\setcounter{MaxMatrixCols}{20}
