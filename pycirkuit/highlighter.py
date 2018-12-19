# -*- coding: utf-8 -*-
"""
Module implementing a Text Highlighter
"""
# Copyright (C) 2018 Orestes Mas
# This file is part of PyCirkuit.
#
# PyCirkuit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCirkuit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
#

# Third-party imports
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat,  QColor


class PyCirkuitHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Variable to hold the formatting rules for each category
        self.highlightingRules = []

        # These are the keywords and patterns to be highlighted, categorized.

        # Formatting rules for punctuation signs
        punctuationFormat = QTextCharFormat()
        punctuationFormat.setFontWeight(QFont.Bold)
        punctuationFormat.setForeground(QColor('sienna'))
        self.highlightingRules.append((QRegExp("[()\{\},;]"), punctuationFormat))
 
        # Formatting rules for operators
        operatorFormat = QTextCharFormat()
        operatorFormat.setFontItalic(True)
        operatorFormat.setForeground(QColor('teal'))
        self.highlightingRules.append((QRegExp("(\+|\-|\*|/|\.|=|<-|->|<->){1,1}"), operatorFormat))
        
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
        "\\batan2\\b","\\bbelow\\b","\\bbetween\\b","\\bbox\\b","\\bby\\b","\\bccw\\b","\\.center\\b", 
        "\\bchop\\b","\\bcircle\\b","\\bcolor\\b","\\bcolour\\b","\\bcolored\\b","\\bcoloured\\b",
        "\\bcommand\\b","\\bcos\\b","\\bcw\\b","\\bdashed\\b","\\bdiam\\b","\\bdo\\b",
        "\\bdotted\\b","\\bdown\\b","\\bellipse\\b","\\belse\\b","\\.end\\b","\\bexp\\b",
        "\\bfill\\b","\\bfor\\b","\\bfrom\\b","\\bheight\\b","\\bht\\b","\\bif\\b",
        "\\binvis(?:ible)?\\b","\\blast\\b","\\bleft\\b","\\bline\\b","\\bljust\\b","\\bmax\\b",
        "\\bmin\\b","\\bmove\\b","\\bof the way between\\b","\\boutline\\b","\\boutlined\\b",
        "\\brad\\b","\\breset\\b","\\bright\\b","\\brjust\\b","\\bshaded\\b","\\bsin\\b",
        "\\bspline\\b","\\bsprintf\\b","\\bsqrt\\b","\\.start\\b","\\btan\\b","\\bthen\\b","\\bthick\\b",
        "\\bto\\b","\\bup\\b","\\bwid\\b","\\bwidth\\b","\\bwith\\b","\\.n\\b","\\.s\\b",
        "\\.e\\b","\\.w\\b","\\.ne\\b","\\.nw\\b","\\.se\\b","\\.sw\\b"]
        picFormat = QTextCharFormat()
        picFormat.setFontItalic(True)
        picFormat.setForeground(QColor('blue'))
        self.highlightingRules.extend([(QRegExp(pattern), picFormat) for pattern in picPatterns])

        # Format for PIC variables: Italic Red
        picVariables = ["\\blinewid\\b","\\blinethick\\b","\\barcrad\\b","\\bcirclerad\\b","\\bellipseht\\b",
        "\\bellipsewid\\b","\\bmoveht\\b","\\bmovewid\\b","\\btextht\\b","\\btextwid\\b","\\barrowht\\b",
        "\\barrowwid\\b","\\barrowhead\\b","\\bdashwid\\b","\\bmaxpswid\\b","\\bmaxpsht\\b","\\bscale\\b",
        "\\bfillval\\b"]
        picFormat = QTextCharFormat()
        picFormat.setFontItalic(True)
        picFormat.setForeground(QColor('red'))
        self.highlightingRules.extend([(QRegExp(pattern), picFormat) for pattern in picVariables])

        # Commands and format for M4 primitives
        m4Patterns = ["\\bchangequote\\b","\\bdefine\\b","\\bdivert\\b","\\bdivnum\\b","\\bdnl\\b","\\bdumpdef\\b",
        "\\berrprint\\b","\\beval\\b","\\bifdef\\b","\\bifelse\\b","\\binclude\\b","\\bincr\\b",
        "\\bindex\\b","\\blen\\b","\\bmaketemp\\b","\\bsinclude\\b","\\bsubstr\\b","\\bsyscmd\\b",
        "\\btranslit\\b","\\bundefine\\b","\\bundivert\\b",]
        m4Format = QTextCharFormat()
        m4Format.setFontWeight(QFont.Bold)
        m4Format.setForeground(QColor('DarkOrchid'))
        self.highlightingRules.extend([(QRegExp(pattern), m4Format) for pattern in m4Patterns])
        
        cmPatterns = ["\\bAND_gate\\b","\\bAND_gen\\b","\\bAND_ht\\b","\\bAND_wd\\b","\\bBOX_gate\\b","\\bBUFFER_gate\\b",
        "\\bBUFFER_gen\\b","\\bBUF_ht\\b","\\bBUF_wd\\b","\\bCos\\b","\\bCosine\\b","\\bDarlington\\b",
        "\\bE_\\b","\\bEquidist3\\b","\\bFF_ht\\b","\\bFF_wid\\b","\\bFector\\b","\\bFlipFlop\\b",
        "\\bFlipFlop6\\b","\\bFlipFlopJK\\b","\\bG_hht_\\b","\\bHOMELIB_\\b","\\bH_ht\\b","\\bInt_\\b",
        "\\bIOdefs\\b","\\bIntersect_\\b","\\bLH_symbol\\b","\\bLoopover_\\b","\\bLT_symbol\\b","\\bL_unit\\b",
        "\\bMax\\b","\\bMin\\b","\\bMux\\b","\\bMux_ht\\b","\\bMux_wid\\b","\\bMx_pins\\b",
        "\\bNAND_gate\\b","\\bNOR_gate\\b","\\bNOT_circle\\b","\\bNOT_gate\\b","\\bNOT_rad\\b","\\bNXOR_gate\\b",
        "\\bN_diam\\b","\\bN_rad\\b","\\bOR_gate\\b","\\bOR_gen\\b","\\bOR_rad\\b","\\bPoint_\\b",
        "\\bRect_\\b","\\bSin\\b","\\bView3D\\b","\\bVperp\\b","\\bXOR_gate\\b","\\bXOR_off\\b",
        "\\babove_\\b","\\babs_\\b","\\badc\\b","\\bamp\\b","\\balong_\\b","\\bantenna\\b",
        "\\barca\\b","\\barcd\\b","\\barcr\\b","\\barcto\\b","\\barrowline\\b","\\bb_\\b",
        "\\bb_current\\b","\\bbattery\\b","\\bbeginshade\\b","\\bbell\\b","\\bbelow_\\b","\\bbi_tr\\b",
        "\\bbi_trans\\b","\\bboxcoord\\b","\\bboxdim\\b","\\bbp__\\b","\\bbswitch\\b","\\bbuzzer\\b",
        "\\bc_fet\\b","\\bcapacitor\\b","\\bcbreaker\\b","\\bcct_init\\b","\\bcintersect\\b","\\bclabel\\b",
        "\\bconsource\\b","\\bcontact\\b","\\bcontline\\b","\\bcorner\\b","\\bcosd\\b","\\bcross\\b","\\bcross3D\\b",
        "\\bcrossover\\b","\\bcrosswd_\\b","\\bcsdim_\\b","\\bdac\\b","\\bd_fet\\b","\\bdabove\\b",
        "\\bdarrow\\b","\\bdarrow_init\\b","\\bdashline\\b","\\bdbelow\\b","\\bdcosine3D\\b","\\bdef_bisect\\b",
        "\\bdelay\\b","\\bdelay_rad_\\b","\\bdeleminit_\\b","\\bdend\\b","\\bdiff3D\\b","\\bdiff_\\b",
        "\\bdimen_\\b","\\bdimension_\\b","\\bdiode\\b","\\bdir_\\b","\\bdistance\\b","\\bdirection_\\b",
        "\\bdistance\\b","\\bdlabel\\b","\\bdleft\\b","\\bdline\\b","\\bdlinewid\\b","\\bdn_\\b",
        "\\bdljust\\b","\\bdn_\\b","\\bdna_\\b","\\bdnm_\\b","\\bdot\\b","\\bdot3D\\b",
        "\\bdotrad_\\b","\\bdown_\\b","\\bdright\\b","\\bdrjust\\b","\\bdswitch\\b","\\bdtee\\b",
        "\\bdtor_\\b","\\bdturn\\b","\\be_\\b","\\be_fet\\b","\\bearphone\\b","\\bebox\\b",
        "\\belchop\\b","\\beleminit_\\b","\\belen_\\b","\\bem_arrows\\b","\\bendshade\\b","\\bexpe\\b",
        "\\bf_box\\b","\\bfill_\\b","\\bfitcurve\\b","\\bfor_\\b","\\bfuse\\b","\\bg_\\b",
        "\\bgap\\b","\\bgen_init\\b","\\bglabel_\\b","\\bgpar_\\b","\\bgpolyline_\\b","\\bgrid_\\b",
        "\\bground\\b","\\bgshade\\b","\\bhoprad_\\b","\\bht_\\b","\\bifdpic\\b","\\bifgpic\\b",
        "\\bifinstr\\b","\\bifmfpic\\b","\\bifmpost\\b","\\bifpgf\\b","\\bifpostscript\\b","\\bifpstricks\\b",
        "\\bifroff\\b","\\bifxfig\\b","\\bigbt\\b","\\bin__\\b","\\binductor\\b","\\binner_prod\\b",
        "\\bintegrator\\b","\\bintersect_\\b","\\bj_fet\\b","\\blarrow\\b","\\blbox\\b","\\bleft_\\b",
        "\\blength3D\\b","\\blg_bartxt\\b","\\blg_pin\\b","\\blg_pintxt\\b","\\blg_plen\\b","\\blin_leng\\b",
        "\\blinethick_\\b","\\bljust_\\b","\\bllabel\\b","\\bloc_\\b","\\blog10E_\\b","\\blog_init\\b",
        "\\bloge\\b","\\blp_xy\\b","\\blpop\\b","\\blswitch\\b","\\blt_\\b","\\bmanhattan\\b",
        "\\bmicrophone\\b","\\bmm__\\b","\\bmosfet\\b","\\bm4xpand\\b","\\bm4lstring\\b","\\bm4_arrow\\b",
        "\\bm4xtract\\b","\\bn_\\b","\\bne_\\b","\\bneg_\\b","\\bnport\\b","\\bnw_\\b",
        "\\bopamp\\b","\\bopen_arrow\\b","\\bpar_\\b","\\bpc__\\b","\\bpi_\\b","\\bpmod\\b",
        "\\bpoint_\\b","\\bpolar_\\b","\\bpotentiometer\\b","\\bprint3D\\b","\\bprod_\\b","\\bproject\\b",
        "\\bpsset_\\b","\\bpt__\\b","\\br_\\b","\\brarrow\\b","\\brect_\\b","\\brelay\\b",
        "\\bresetrgb\\b","\\bresistor\\b","\\breversed\\b","\\brgbdraw\\b","\\brgbfill\\b","\\bright_\\b",
        "\\brjust_\\b","\\brlabel\\b","\\brot3Dx\\b","\\brot3Dy\\b","\\brot3Dz\\b","\\brpoint_\\b",
        "\\brpos_\\b","\\brrot_\\b","\\brs_box\\b","\\brsvec_\\b","\\brt_\\b","\\brtod_\\b",
        "\\brtod__\\b","\\brvec_\\b","\\bs_\\b","\\bs_box\\b","\\bs_dp\\b","\\bs_ht\\b",
        "\\bs_init\\b","\\bs_name\\b","\\bs_wd\\b","\\bsc_draw\\b","\\bse_\\b","\\bsetrgb\\b",
        "\\bsetview\\b","\\bsfg_init\\b","\\bsfgabove\\b","\\bsfgarc\\b","\\bsfgbelow\\b","\\bsfgline\\b",
        "\\bsfgnode\\b","\\bsfgself\\b","\\bshade\\b","\\bshadebox\\b","\\bsign_\\b","\\bsinc\\b",
        "\\bsind\\b","\\bsinusoid\\b","\\bsource\\b","\\bsourcerad_\\b","\\bsp_\\b","\\bspeaker\\b",
        "\\bsprod3D\\b","\\bsum3D\\b","\\bsum_\\b","\\bsvec_\\b","\\bsw_\\b","\\bswitch\\b",
        "\\bta_xy\\b","\\bthicklines_\\b","\\bthinlines_\\b","\\bthyristor\\b","\\btline\\b","\\btr_xy\\b",
        "\\btr_xy_init\\b","\\btransformer\\b","\\bttmotor\\b","\\btwopi_\\b","\\bujt\\b","\\bunit3D\\b",
        "\\bup_\\b","\\bup__\\b","\\bvariable\\b","\\bvec_\\b","\\bvlength\\b","\\bvperp\\b",
        "\\bvrot_\\b","\\bvscal_\\b","\\bw_\\b","\\bwid_\\b","\\bwinding\\b","\\bxtal\\b",
        "\\bxtract\\b",]
        cmFormat = QTextCharFormat()
        cmFormat.setFontWeight(QFont.Bold)
        cmFormat.setForeground(QColor('DarkGreen'))
        self.highlightingRules.extend([(QRegExp(pattern), cmFormat) for pattern in cmPatterns])

        # Comments are displayed in gray
        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor('DarkGray'))
        self.highlightingRules.append((QRegExp("#[^\n]*"), singleLineCommentFormat))


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


