# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat,  QColor


class PyCirkuitHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PyCirkuitHighlighter, self).__init__(parent)

        # Variable to hold the formatting rules for each category
        self.highlightingRules = []

        # These are the keywords and patterns to be highlighted, categorized.

        # Comments are displayed in gray
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor('darkgray'))
        self.highlightingRules.append((QRegExp("#[^\n]*"), singleLineCommentFormat))

        # Formatting rules for punctuation signs
        punctuationFormat = QTextCharFormat()
        punctuationFormat.setForeground(QColor('sienna'))
        self.highlightingRules.append((QRegExp("[(),;]"), punctuationFormat))
 
        # Formatting rules for operators
        operatorFormat = QTextCharFormat()
        operatorFormat.setFontWeight(QFont.Bold)
        operatorFormat.setForeground(QColor('navy'))
        self.highlightingRules.append((QRegExp("[+-*/\.]"), operatorFormat))
        
        # Label displaying rules
        labelFormat = QTextCharFormat()
        labelFormat.setFontWeight(QFont.Bold)
        labelFormat.setForeground(QColor('deeppink'))
        self.highlightingRules.append((QRegExp("[A-Z]+[A-Za-z0-9]*:"), labelFormat))

        # String displaying rules
        stringFormat = QTextCharFormat()
        stringFormat.setFontWeight(QFont.Bold)
        stringFormat.setForeground(QColor('firebrick'))
        self.highlightingRules.append((QRegExp('\".*\"'), stringFormat))

        # Now the beggining and ending PIC commands in red
        picBoundaryPatterns = ["^\.P[SE]{1,1}\\b"]
        picBoundaryFormat = QTextCharFormat()
        picBoundaryFormat.setForeground(QColor('darkred'))
        self.highlightingRules.extend([(QRegExp(pattern), picBoundaryFormat)
                for pattern in picBoundaryPatterns])
    
        # Format for PIC commands: Italic Blue
        picPatterns = ["\\b1st\\b","\\b2nd\\b","\\b3rd\\b","\\b4th\\b","\\b5th\\b","\\b6th\\b",
        "\\b7th\\b","\\b8th\\b","\\b9th\\b","\\bHere\\b","\\babove\\b","\\band\\b",
        "\\barc\\b","\\barrow\\b","\\barrowhead\\b","\\barrowht\\b","\\barrowwid\\b","\\bat\\b",
        "\\batan2\\b","\\bbelow\\b","\\bbetween\\b","\\bbox\\b","\\bby\\b","\\bccw\\b",
        "\\bchop\\b","\\bcircle\\b","\\bcolor\\b","\\bcolour\\b","\\bcolored\\b","\\bcoloured\\b",
        "\\bcommand\\b","\\bcos\\b","\\bcw\\b","\\bdashed\\b","\\bdiam\\b","\\bdo\\b",
        "\\bdotted\\b","\\bdown\\b","\\bellipse\\b","\\belse\\b","\\bend\\b","\\bexp\\b",
        "\\bfill\\b","\\bfor\\b","\\bfrom\\b","\\bheight\\b","\\bht\\b","\\bif\\b",
        "\\binvis\\b","\\blast\\b","\\bleft\\b","\\bline\\b","\\bljust\\b","\\bmax\\b",
        "\\bmin\\b","\\bmove\\b","\\boutline\\b","\\boutlined\\b","\\brad\\b","\\breset\\b",
        "\\bright\\b","\\brjust\\b","\\bscale\\b","\\bshaded\\b","\\bsin\\b","\\bspline\\b",
        "\\bsprintf\\b","\\bsqrt\\b","\\bstart\\b","\\btan\\b","\\bthen\\b","\\bthick\\b",
        "\\bto\\b","\\bup\\b","\\bwid\\b","\\bwidth\\b","\\bwith\\b",]
        picFormat = QTextCharFormat()
        picFormat.setFontItalic(True)
        picFormat.setForeground(QColor('blue'))
        self.highlightingRules.extend([(QRegExp(pattern), picFormat) for pattern in picPatterns])

        # Commands and format for M4 primitives
        m4Patterns = ["\\bchangequote","\\bdefine","\\bdivert","\\bdivnum","\\bdnl","\\bdumpdef",
        "\\berrprint","\\beval","\\bifdef","\\bifelse","\\binclude","\\bincr",
        "\\bindex","\\blen","\\bmaketemp","\\bsinclude","\\bsubstr","\\bsyscmd",
        "\\btranslit","\\bundefine","\\bundivert",]
        m4Format = QTextCharFormat()
        m4Format.setFontItalic(True)
        m4Format.setForeground(QColor('darkmagenta'))
        self.highlightingRules.extend([(QRegExp(pattern), picFormat) for pattern in m4Patterns])
        
        cmPatterns = ["\\bAND_gate","\\bAND_gen","\\bAND_ht","\\bAND_wd","\\bBOX_gate","\\bBUFFER_gate",
        "\\bBUFFER_gen","\\bBUF_ht","\\bBUF_wd","\\bCos","\\bCosine","\\bDarlington",
        "\\bE_","\\bEquidist3","\\bFF_ht","\\bFF_wid","\\bFector","\\bFlipFlop",
        "\\bFlipFlop6","\\bFlipFlopJK","\\bG_hht_","\\bHOMELIB_","\\bH_ht","\\bInt_",
        "\\bIOdefs","\\bIntersect_","\\bLH_symbol","\\bLoopover_","\\bLT_symbol","\\bL_unit",
        "\\bMax","\\bMin","\\bMux","\\bMux_ht","\\bMux_wid","\\bMx_pins",
        "\\bNAND_gate","\\bNOR_gate","\\bNOT_circle","\\bNOT_gate","\\bNOT_rad","\\bNXOR_gate",
        "\\bN_diam","\\bN_rad","\\bOR_gate","\\bOR_gen","\\bOR_rad","\\bPoint_",
        "\\bRect_","\\bSin","\\bView3D","\\bVperp","\\bXOR_gate","\\bXOR_off",
        "\\babove_","\\babs_","\\badc","\\bamp","\\balong_","\\bantenna",
        "\\barca","\\barcd","\\barcr","\\barcto","\\barrowline","\\bb_",
        "\\bb_current","\\bbattery","\\bbeginshade","\\bbell","\\bbelow_","\\bbi_tr",
        "\\bbi_trans","\\bboxcoord","\\bboxdim","\\bbp__","\\bbswitch","\\bbuzzer",
        "\\bc_fet","\\bcapacitor","\\bcbreaker","\\bcct_init","\\bcintersect","\\bclabel",
        "\\bconsource","\\bcontact","\\bcontline","\\bcorner","\\bcosd","\\bcross","\\bcross3D",
        "\\bcrossover","\\bcrosswd_","\\bcsdim_","\\bdac","\\bd_fet","\\bdabove",
        "\\bdarrow","\\bdarrow_init","\\bdashline","\\bdbelow","\\bdcosine3D","\\bdef_bisect",
        "\\bdelay","\\bdelay_rad_","\\bdeleminit_","\\bdend","\\bdiff3D","\\bdiff_",
        "\\bdimen_","\\bdimension_","\\bdiode","\\bdir_","\\bdistance","\\bdirection_",
        "\\bdistance","\\bdlabel","\\bdleft","\\bdline","\\bdlinewid","\\bdn_",
        "\\bdljust","\\bdn_","\\bdna_","\\bdnm_","\\bdot","\\bdot3D",
        "\\bdotrad_","\\bdown_","\\bdright","\\bdrjust","\\bdswitch","\\bdtee",
        "\\bdtor_","\\bdturn","\\be_","\\be_fet","\\bearphone","\\bebox",
        "\\belchop","\\beleminit_","\\belen_","\\bem_arrows","\\bendshade","\\bexpe",
        "\\bf_box","\\bfill_","\\bfitcurve","\\bfor_","\\bfuse","\\bg_",
        "\\bgap","\\bgen_init","\\bglabel_","\\bgpar_","\\bgpolyline_","\\bgrid_",
        "\\bground","\\bgshade","\\bhoprad_","\\bht_","\\bifdpic","\\bifgpic",
        "\\bifinstr","\\bifmfpic","\\bifmpost","\\bifpgf","\\bifpostscript","\\bifpstricks",
        "\\bifroff","\\bifxfig","\\bigbt","\\bin__","\\binductor","\\binner_prod",
        "\\bintegrator","\\bintersect_","\\bj_fet","\\blarrow","\\blbox","\\bleft_",
        "\\blength3D","\\blg_bartxt","\\blg_pin","\\blg_pintxt","\\blg_plen","\\blin_leng",
        "\\blinethick_","\\bljust_","\\bllabel","\\bloc_","\\blog10E_","\\blog_init",
        "\\bloge","\\blp_xy","\\blpop","\\blswitch","\\blt_","\\bmanhattan",
        "\\bmicrophone","\\bmm__","\\bmosfet","\\bm4xpand","\\bm4lstring","\\bm4_arrow",
        "\\bm4xtract","\\bn_","\\bne_","\\bneg_","\\bnport","\\bnw_",
        "\\bopamp","\\bopen_arrow","\\bpar_","\\bpc__","\\bpi_","\\bpmod",
        "\\bpoint_","\\bpolar_","\\bpotentiometer","\\bprint3D","\\bprod_","\\bproject",
        "\\bpsset_","\\bpt__","\\br_","\\brarrow","\\brect_","\\brelay",
        "\\bresetrgb","\\bresistor","\\breversed","\\brgbdraw","\\brgbfill","\\bright_",
        "\\brjust_","\\brlabel","\\brot3Dx","\\brot3Dy","\\brot3Dz","\\brpoint_",
        "\\brpos_","\\brrot_","\\brs_box","\\brsvec_","\\brt_","\\brtod_",
        "\\brtod__","\\brvec_","\\bs_","\\bs_box","\\bs_dp","\\bs_ht",
        "\\bs_init","\\bs_name","\\bs_wd","\\bsc_draw","\\bse_","\\bsetrgb",
        "\\bsetview","\\bsfg_init","\\bsfgabove","\\bsfgarc","\\bsfgbelow","\\bsfgline",
        "\\bsfgnode","\\bsfgself","\\bshade","\\bshadebox","\\bsign_","\\bsinc",
        "\\bsind","\\bsinusoid","\\bsource","\\bsourcerad_","\\bsp_","\\bspeaker",
        "\\bsprod3D","\\bsum3D","\\bsum_","\\bsvec_","\\bsw_","\\bswitch",
        "\\bta_xy","\\bthicklines_","\\bthinlines_","\\bthyristor","\\btline","\\btr_xy",
        "\\btr_xy_init","\\btransformer","\\bttmotor","\\btwopi_","\\bujt","\\bunit3D",
        "\\bup_","\\bup__","\\bvariable","\\bvec_","\\bvlength","\\bvperp",
        "\\bvrot_","\\bvscal_","\\bw_","\\bwid_","\\bwinding","\\bxtal",
        "\\bxtract",]
        cmFormat = QTextCharFormat()
        cmFormat.setFontWeight(QFont.Bold)
        cmFormat.setForeground(QColor('darkgreen'))
        self.highlightingRules.extend([(QRegExp(pattern), cmFormat) for pattern in cmPatterns])


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
#
#        self.setCurrentBlockState(0)
#
#        startIndex = 0
#        if self.previousBlockState() != 1:
#            startIndex = self.commentStartExpression.indexIn(text)
#
#        while startIndex >= 0:
#            endIndex = self.commentEndExpression.indexIn(text, startIndex)
#
#            if endIndex == -1:
#                self.setCurrentBlockState(1)
#                commentLength = len(text) - startIndex
#            else:
#                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()
#
#            self.setFormat(startIndex, commentLength,
#                    self.multiLineCommentFormat)
#            startIndex = self.commentStartExpression.indexIn(text,
#                    startIndex + commentLength);

