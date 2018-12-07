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


from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat


class PyCirkuitHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PyCirkuitHighlighter, self).__init__(parent)

        #FIXME: Change all the rules

        # Keyword formatting rules: DarkBlue Bold
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)
        # These are the keywords
        keywordPatterns = ["\\bPS","\\bPE","\\bchangequote","\\bdefine","\\bdivert","\\bdivnum",
        "\\bdnl","\\bdumpdef","\\berrprint","\\beval","\\bifdef","\\bifelse","\\binclude",
        "\\bincr","\\bindex","\\blen","\\bmaketemp","\\bsinclude","\\bsubstr","\\bsyscmd",
        "\\btranslit","\\bundefine","\\bundivert","\\b1st","\\b2nd","\\b3rd","\\b4th","\\b5th",
        "\\b6th","\\b7th","\\b8th","\\b9th","\\bHere","\\babove","\\band","\\barc","\\barrow",
        "\\barrowhead","\\barrowht","\\barrowwid","\\bat","\\batan2","\\bbelow","\\bbetween",
        "\\bbox","\\bby","\\bccw","\\bchop","\\bcircle","\\bcolor","\\bcolour","\\bcolored",
        "\\bcoloured","\\bcommand","\\bcos","\\bcw","\\bdashed","\\bdiam","\\bdo","\\bdotted",
        "\\bdown","\\bellipse","\\belse","\\bend","\\bexp","\\bfill","\\bfor","\\bfrom","\\bheight",
        "\\bht","\\bif","\\binvis","\\blast","\\bleft","\\bline","\\bljust","\\bmax","\\bmin",
        "\\bmove","\\boutline","\\boutlined","\\brad","\\breset","\\bright","\\brjust","\\bscale",
        "\\bshaded","\\bsin","\\bspline","\\bsprintf","\\bsqrt","\\bstart","\\btan","\\bthen",
        "\\bthick","\\bto","\\bup","\\bwid","\\bwidth","\\bwith","\\bAND_gate","\\bAND_gen",
        "\\bAND_ht","\\bAND_wd","\\bBOX_gate","\\bBUFFER_gate","\\bBUFFER_gen","\\bBUF_ht",
        "\\bBUF_wd","\\bCos","\\bCosine","\\bDarlington","\\bE_","\\bEquidist3","\\bFF_ht",
        "\\bFF_wid","\\bFector","\\bFlipFlop","\\bFlipFlop6","\\bFlipFlopJK","\\bG_hht_",
        "\\bHOMELIB_","\\bH_ht","\\bInt_","\\bIOdefs","\\bIntersect_","\\bLH_symbol","\\bLoopover_",
        "\\bLT_symbol","\\bL_unit","\\bMax","\\bMin","\\bMux","\\bMux_ht","\\bMux_wid","\\bMx_pins",
        "\\bNAND_gate","\\bNOR_gate","\\bNOT_circle","\\bNOT_gate","\\bNOT_rad","\\bNXOR_gate",
        "\\bN_diam","\\bN_rad","\\bOR_gate","\\bOR_gen","\\bOR_rad","\\bPoint_","\\bRect_","\\bSin",
        "\\bView3D","\\bVperp","\\bXOR_gate","\\bXOR_off","\\babove_","\\babs_","\\badc","\\bamp",
        "\\balong_","\\bantenna","\\barca","\\barcd","\\barcr","\\barcto","\\barrowline","\\bb_",
        "\\bb_current","\\bbattery","\\bbeginshade","\\bbell","\\bbelow_","\\bbi_tr","\\bbi_trans",
        "\\bboxcoord","\\bboxdim","\\bbp__","\\bbswitch","\\bbuzzer","\\bc_fet","\\bcapacitor",
        "\\bcbreaker","\\bcct_init","\\bcintersect","\\bclabel","\\bconsource","\\bcontact",
        "\\bcontline","\\bcosd","\\bcross","\\bcross3D","\\bcrossover","\\bcrosswd_","\\bcsdim_",
        "\\bdac","\\bd_fet","\\bdabove","\\bdarrow","\\bdarrow_init","\\bdashline","\\bdbelow",
        "\\bdcosine3D","\\bdef_bisect","\\bdelay","\\bdelay_rad_","\\bdeleminit_","\\bdend",
        "\\bdiff3D","\\bdiff_","\\bdimen_","\\bdimension_","\\bdiode","\\bdir_","\\bdistance",
        "\\bdirection_","\\bdistance","\\bdlabel","\\bdleft","\\bdline","\\bdlinewid","\\bdn_",
        "\\bdljust","\\bdn_","\\bdna_","\\bdnm_","\\bdot","\\bdot3D","\\bdotrad_","\\bdown_",
        "\\bdright","\\bdrjust","\\bdswitch","\\bdtee","\\bdtor_","\\bdturn","\\be_","\\be_fet",
        "\\bearphone","\\bebox","\\belchop","\\beleminit_","\\belen_","\\bem_arrows","\\bendshade",
        "\\bexpe","\\bf_box","\\bfill_","\\bfitcurve","\\bfor_","\\bfuse","\\bg_","\\bgap",
        "\\bgen_init","\\bglabel_","\\bgpar_","\\bgpolyline_","\\bgrid_","\\bground","\\bgshade",
        "\\bhoprad_","\\bht_","\\bifdpic","\\bifgpic","\\bifinstr","\\bifmfpic","\\bifmpost",
        "\\bifpgf","\\bifpostscript","\\bifpstricks","\\bifroff","\\bifxfig","\\bigbt","\\bin__",
        "\\binductor","\\binner_prod","\\bintegrator","\\bintersect_","\\bj_fet","\\blarrow",
        "\\blbox","\\bleft_","\\blength3D","\\blg_bartxt","\\blg_pin","\\blg_pintxt","\\blg_plen",
        "\\blin_leng","\\blinethick_","\\bljust_","\\bllabel","\\bloc_","\\blog10E_","\\blog_init",
        "\\bloge","\\blp_xy","\\blpop","\\blswitch","\\blt_","\\bmanhattan","\\bmicrophone","\\bmm__",
        "\\bmosfet","\\bm4xpand","\\bm4lstring","\\bm4_arrow","\\bm4xtract","\\bn_","\\bne_","\\bneg_",
        "\\bnport","\\bnw_","\\bopamp","\\bopen_arrow","\\bpar_","\\bpc__","\\bpi_","\\bpmod","\\bpoint_",
        "\\bpolar_","\\bpotentiometer","\\bprint3D","\\bprod_","\\bproject","\\bpsset_","\\bpt__","\\br_",
        "\\brarrow","\\brect_","\\brelay","\\bresetrgb","\\bresistor","\\breversed","\\brgbdraw",
        "\\brgbfill","\\bright_","\\brjust_","\\brlabel","\\brot3Dx","\\brot3Dy","\\brot3Dz",
        "\\brpoint_","\\brpos_","\\brrot_","\\brs_box","\\brsvec_","\\brt_","\\brtod_","\\brtod__",
        "\\brvec_","\\bs_","\\bs_box","\\bs_dp","\\bs_ht","\\bs_init","\\bs_name","\\bs_wd","\\bsc_draw",
        "\\bse_","\\bsetrgb","\\bsetview","\\bsfg_init","\\bsfgabove","\\bsfgarc","\\bsfgbelow",
        "\\bsfgline","\\bsfgnode","\\bsfgself","\\bshade","\\bshadebox","\\bsign_","\\bsinc","\\bsind",
        "\\bsinusoid","\\bsource","\\bsourcerad_","\\bsp_","\\bspeaker","\\bsprod3D","\\bsum3D","\\bsum_",
        "\\bsvec_","\\bsw_","\\bswitch","\\bta_xy","\\bthicklines_","\\bthinlines_","\\bthyristor",
        "\\btline","\\btr_xy","\\btr_xy_init","\\btransformer","\\bttmotor","\\btwopi_","\\bujt",
        "\\bunit3D","\\bup_","\\bup__","\\bvariable","\\bvec_","\\bvlength","\\bvperp","\\bvrot_",
        "\\bvscal_","\\bw_","\\bwid_","\\bwinding","\\bxtal","\\bxtract"]
        
        # Create a list structure containing the highlighting rules.
        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        # Now the begining and ending PIC commands
        picBoundaryFormat = QTextCharFormat()
        picBoundaryFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("^\.P[SE]{1,1}\\b"),
                picBoundaryFormat))

        # Now the formatting rules for the classes
        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        # Comments are displayed in gray
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.gray)
        self.highlightingRules.append((QRegExp("#[^\n]*"),
                singleLineCommentFormat))

#        # Format for functions: Italic Blue
#        functionFormat = QTextCharFormat()
#        functionFormat.setFontItalic(True)
#        functionFormat.setForeground(Qt.blue)
#        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
#                functionFormat))

#        self.commentStartExpression = QRegExp("/\\*")
#        self.commentEndExpression = QRegExp("\\*/")

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

