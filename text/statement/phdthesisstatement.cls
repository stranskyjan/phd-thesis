%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% LaTeX template for PhD thesis statement
%
% (C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\message{*******************************************************************}
\message{LaTeX template for PhD thesis statement}
\message{(C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)}
\message{*******************************************************************}

\NeedsTeXFormat{LaTeX2e}%[1996/12/01]
\ProvidesClass{phdthesisstatement}[2018/01/31 PhD thesis statement class]

\newcommand{\showframe}{false}
\DeclareOption{showframe}{\renewcommand{\showframe}{true}}
\ProcessOptions\relax

\LoadClass[12pt,twoside]{report}

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
\RequirePackage{import}
\RequirePackage{graphicx}

\RequirePackage[main=english,czech]{babel}
\RequirePackage[unicode]{hyperref}
\RequirePackage{multirow}
\RequirePackage{hyphenat}
\RequirePackage{url}

\RequirePackage{csquotes}

\RequirePackage[style=numeric,giveninits=true,backend=biber,maxnames=99]{biblatex}
\DeclareFieldFormat[article]{title}{#1}
\renewbibmacro{in:}{\ifentrytype{article}{}{\printtext{\bibstring{in}\intitlepunct}}}

\newcommand{\cleardoublepageempty}{%
	\newpage%
	\pagestyle{empty}%
	\cleardoublepage%
	\pagestyle{main}%
}
\newcommand{\blankpage}{\newpage\null\thispagestyle{empty}\newpage}
\newcommand{\doubleblankpage}{\blankpage\blankpage}

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
\renewcommand{\part}[1]{
	\cleardoublepageempty
	\pagestyle{empty}
	\doubleblankpage%
	\partOrig{#1}%
	\pagestyle{main}%
}

\RequirePackage{titleps}
\newpagestyle{main}{%
	\setheadrule{.7pt}%
	\sethead*{%
		\sc%
		\ifthenelse{\equal{\mypagestyle}{nonumber}}{}{\thechapter\ \ }%
		\chaptertitle}{}{\thepage}%
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

\makeatletter
\newcommand{\mydotfill}[1]{\leavevmode \cleaders \hb@xt@ #1{\hss .\hss }\hfill \kern \z@}
\makeatother


\RequirePackage[%
	labelsep=colon,%
	justification=centering,%
	margin=1cm,%
	figureposition=below,%
	tableposition=above%
]{caption}


\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}

\pdfsuppresswarningpagegroup=1

\RequirePackage{xstring}
\RequirePackage{xcolor}
