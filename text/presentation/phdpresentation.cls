%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% LaTeX template for PhD thesis presentation
%
% (C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\message{*******************************************************************}
\message{LaTeX template for PhD thesis presentation}
\message{(C) 2018  Jan Stránský  (jan.stransky@fsv.cvut.cz)}
\message{*******************************************************************}

\NeedsTeXFormat{LaTeX2e}%[1996/12/01]
\ProvidesClass{phdpresentation}[2018/04/26 PhD thesis presentation class]

\LoadClassWithOptions{beamer}

\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[czech,english]{babel}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{graphicx}
\RequirePackage{xstring}

\mode<presentation>
\mode<all>

\setbeamercovered{transparent}

% footline
\setbeamertemplate{footline}{\hfill\insertframenumber{} / \inserttotalframenumber{}\hspace{3mm}\strut}
\setbeamercolor{footline}{fg=gray}
\beamertemplatenavigationsymbolsempty

% color stuff
\definecolor{ctuBlue}{RGB}{0,101,189}
\definecolor{ctuRed}{RGB}{198,12,48}
\definecolor{ctuLightBlue}{RGB}{106,173,228}
\definecolor{blockGray}{RGB}{240,240,240}
\setbeamercolor{structure}{fg=ctuBlue}
\setbeamercolor{block title}{bg=ctuBlue,fg=white}
\setbeamercolor{block body}{bg=blockGray}

% set size
\setbeamersize{text margin left=2.9em,text margin right=2em}

% fonts
\renewcommand{\familydefault}{\sfdefault}
\RequirePackage[scaled]{helvet}
\RequirePackage[helvet]{sfmath}
\setbeamerfont{title page}{series=\bfseries}
\setbeamerfont{headline}{series=\bfseries}
\setbeamerfont{block title}{series=\bfseries}
\setbeamerfont{footline}{size=\footnotesize}
\AtBeginDocument{\bfseries\selectfont} % normal text 

% background
\setbeamertemplate{background canvas}{%
	\ifnum\c@framenumber=1% first slide
		\includegraphics[width=\paperwidth,height=\paperheight]{figs/raphaelpy/background0}
	\else% other slides
		\includegraphics[width=\paperwidth,height=\paperheight]{figs/raphaelpy/background1}
	\fi%
}

% bullets, itemize
\useinnertheme{rectangles}
\newenvironment{myitemize}{%
	\vspace{-.3em}
	\begin{itemize}
	\setlength{\itemsep}{0pt}
}{%
	\end{itemize}
	\vspace{-.3em}
}

% title page
\setbeamertemplate{title page}{
	\begin{columns}
		\begin{column}{1.3em}
		\end{column}
		\begin{column}{\dimexpr\textwidth-1.3em}
			\color{white}
			{\LARGE\inserttitle\par}
			\vspace{10mm}
			\insertauthor\par
			\insertinstitute\par
			\insertdate
		\end{column}
	\end{columns}
}

% headline and frametitle
\setbeamertemplate{frametitle}{}
\setbeamertemplate{headline}{%
	\hbox{%
		\begin{beamercolorbox}[wd=0.95\paperwidth,ht=1.5cm, right]{headline}%
			\small
			\MakeUppercase{\insertframetitle}\strut\par
			\vspace{1mm}
			\MakeUppercase{\insertframesubtitle}\strut\par
			\vfill
		\end{beamercolorbox}%
	}
}

% to make \setbeamertemplate work ...
\def\insertframetitle{}
\def\insertframesubtitle{}


\AtBeginDocument{%
	\part{Presentation}
}

\AtBeginSection{%
	{
	\setbeamertemplate{footline}{} 
	\begin{frame}
		\tableofcontents[currentsection,hideallsubsections]
	\end{frame}
	\addtocounter{framenumber}{-1}
	}
}

% discussion
\newenvironment{discussion}{
	\part{Discussion}
   \newcounter{framenumberappendix}
   \setcounter{framenumberappendix}{\value{framenumber}}
	\setbeamertemplate{footline}{}
	\begin{frame}
	\end{frame}
	\AtBeginSection{}
}{
   \addtocounter{framenumberappendix}{-\value{framenumber}}
   \addtocounter{framenumber}{\value{framenumberappendix}} 
}

\newenvironment{questionblock}{
	\begin{block}{Question}
	\footnotesize
}{
	\end{block}
}

\newenvironment{answerblock}{
	\begin{block}{Answer}
}{
	\end{block}
}

\newenvironment{questionframe}[1]{
	\subsection{Question #1}
	\begin{frame}
		\frametitle{Discussion}
		\framesubtitle{\secname, \subsecname}
}{
	\end{frame}
}

% outlineframe
\newcommand{\outlineframe}{%
	\begin{frame}
		\frametitle{Outline}
		\tableofcontents[hideallsubsections]
	\end{frame}
}

% twocolumn layout
\newcounter{twocolumncounter}
\newenvironment{twocolumns}{%
	\setcounter{twocolumncounter}{0}%
	\begin{columns}[onlytextwidth,totalwidth=1.033\textwidth]%
}{%
	\end{columns}%
}
\let\onecolumn\undefined
\newenvironment{onecolumn}{%
	\ifthenelse{\value{twocolumncounter}=0}{}{\hfill}%
	\addtocounter{twocolumncounter}{1}%
	\begin{column}{.475\textwidth}%
}{%
	\end{column}%
}
