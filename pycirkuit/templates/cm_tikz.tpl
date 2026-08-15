%%backend=circuitmacros%%
\documentclass{article}
\usepackage{fontspec}

% Uncomment and adapt if you want language support other than English.
%\usepackage[catalan]{babel}

% Default font is Latin Modern (fontspec's default, visually equivalent to
% Computer Modern). To use a different font, uncomment and adapt the lines
% below to your chosen family.
%\setmainfont{Libertinus Serif}
%\setsansfont{Libertinus Sans}
%\usepackage{unicode-math}
%\setmathfont{Libertinus Math}

\usepackage{siunitx}
\sisetup{
    output-decimal-marker = {,},
    per-mode = symbol,
    group-separator = {.},
    output-complex-root = \ensuremath{\mathrm{j}},
    binary-units
}
\DeclareSIUnit[number-unit-product = \,]\dBV{\deci\bel V}
\DeclareSIUnit[number-unit-product = \,]\dBuV{\deci\bel\mu V}

\usepackage{tikz,amsmath}
\usetikzlibrary{arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks}

\usepackage[tightpage,active,pdftex]{preview}
\PreviewEnvironment{tikzpicture}
\newlength{\imagewidth}
\newlength{\imagescale}
\pagestyle{empty}

\newcommand{\fasor}[1]{\ensuremath{\mathbf{\overline{#1}}}}

\begin{document}
\thispagestyle{empty}
%%SOURCE%%
\end{document}
