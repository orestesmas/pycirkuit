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
        keywordPatterns = ["\\bresistor\\b", "\\binductor\\b", "\\bcapacitor\\b",
                "\\bopamp\\b"]
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

