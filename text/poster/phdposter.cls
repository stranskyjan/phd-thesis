%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% LaTeX template for PhD thesis poster
%
% (C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\message{*******************************************************************}
\message{LaTeX template for PhD thesis poster}
\message{(C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)}
\message{*******************************************************************}

\NeedsTeXFormat{LaTeX2e}%[1996/12/01]
\ProvidesClass{phdposter}[2018/01/31 PhD thesis poster class]

\LoadClass{article}

\RequirePackage{cmap}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[unicode]{hyperref}
\RequirePackage[%
	%showframe,%
	b1paper,%
	inner=3cm,%
	outer=3cm,%
	top=3cm,%
	bottom=3cm,%
]{geometry}
\RequirePackage[table]{xcolor}
\RequirePackage{tabu}
\RequirePackage{pagecolor}
\RequirePackage{graphicx}

\renewcommand{\familydefault}{\sfdefault}
\RequirePackage[scaled]{helvet}
\RequirePackage[helvet]{sfmath}

\AtBeginDocument{%
	\normalsize
	\renewcommand{\arraystretch}{1.0}
}
\renewcommand{\tiny}{\fontsize{14.40}{18} \selectfont}
\renewcommand{\scriptsize}{\fontsize{17.28}{22}\selectfont}
\renewcommand{\footnotesize}{\fontsize{20.74}{25}\selectfont}
\renewcommand{\small}{\fontsize{24.88}{30}\selectfont}
\renewcommand{\normalsize}{\fontsize{29.86}{37}\selectfont}
\renewcommand{\large}{\fontsize{35.83}{45}\selectfont}
\renewcommand{\Large}{\fontsize{43.00}{54}\selectfont}
\renewcommand{\LARGE}{\fontsize{51.60}{64}\selectfont}
\renewcommand{\huge}{\fontsize{61.92}{77}\selectfont}
\renewcommand{\Huge}{\fontsize{74.30}{93}\selectfont}
\newcommand{\veryHuge}{\fontsize{89.16}{112}\selectfont}
\newcommand{\VeryHuge}{\fontsize{107.0}{134}\selectfont}

\definecolor{ctu}{RGB}{0,101,189}
\tabulinesep=1.5em
\taburowcolors 2{ctu .. ctu!20}
\tabcolsep=1.5em
\pagecolor{black!20}
\pagecolor{white}

\newenvironment{posterframe}[2]{
	\noindent
	\begin{tabu} to #1 {X}
	\rule[-.3em]{.0em}{1.3em}
	\textbf{\large \color{white}{#2}}
	\\
}{
	\end{tabu}%
}

\pagestyle{empty}

\newcommand{\postertitle}{
	\begin{center}
		\LARGE\textbf\thesisTitle\par
	\end{center}
	\vspace{.9em}
	\begin{minipage}{.2\textwidth}
		\centering
		\includegraphics[height=5cm]{ctu_logo}
	\end{minipage}
	\hfill
	\begin{minipage}{.79\textwidth}
		\Large
		\textbf{\authorDegree\ \authorName}, Supervisor: \textbf{\supervisor}\par
		\large
		\department,
		\faculty,
		\university
		\par
		Period of doctoral study: \periodOfDoctoralStudy\par
	\end{minipage}
	\par
	\vspace{.018\textwidth}
	\noindent\makebox[\linewidth]{\color{ctu}\rule{\paperwidth}{2mm}}
	\par
	\vspace{.018\textwidth}
}

\newcommand{\postervspace}{\par\vspace{.018\paperwidth}\par}

\RequirePackage{anyfontsize}

\RequirePackage{enumitem}
\setlist[itemize,enumerate]{nolistsep}

\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
