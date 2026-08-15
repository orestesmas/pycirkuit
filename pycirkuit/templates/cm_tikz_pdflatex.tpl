%%backend=circuitmacros%%
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}

% Uncomment and adapt if you want language support other than English.
%\usepackage[catalan]{babel}

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
