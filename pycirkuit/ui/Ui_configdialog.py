# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/orestes/Devel/Software/pycirkuit/pycirkuit/ui/configdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName("ConfigDialog")
        ConfigDialog.resize(899, 561)
        ConfigDialog.setMinimumSize(QtCore.QSize(800, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfigDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(ConfigDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QtCore.QSize(128, 16777215))
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setStyleSheet(
            "padding-top: 10px; \n" "background-color: rgb(255, 255, 255);"
        )
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.listWidget.setIconSize(QtCore.QSize(48, 48))
        self.listWidget.setTextElideMode(QtCore.Qt.ElideNone)
        self.listWidget.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget.setProperty("isWrapping", True)
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setWordWrap(True)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/pixmaps/CfgGeneral"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        item.setIcon(icon)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/pixmaps/CfgExportImage"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        item.setIcon(icon1)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        self.horizontalLayout.addWidget(self.listWidget)
        self.stackedWidget = QtWidgets.QStackedWidget(ConfigDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stackedWidget.sizePolicy().hasHeightForWidth()
        )
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setBaseSize(QtCore.QSize(0, 0))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.page1)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cmPath = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmPath.sizePolicy().hasHeightForWidth())
        self.cmPath.setSizePolicy(sizePolicy)
        self.cmPath.setClearButtonEnabled(True)
        self.cmPath.setObjectName("cmPath")
        self.horizontalLayout_3.addWidget(self.cmPath)
        self.toolButtonCMPath = QtWidgets.QToolButton(self.groupBox)
        self.toolButtonCMPath.setMinimumSize(QtCore.QSize(120, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/Open"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.toolButtonCMPath.setIcon(icon2)
        self.toolButtonCMPath.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonCMPath.setObjectName("toolButtonCMPath")
        self.horizontalLayout_3.addWidget(self.toolButtonCMPath)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.groupBox_2 = QtWidgets.QGroupBox(self.page1)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.templateFile = QtWidgets.QLineEdit(self.groupBox_2)
        self.templateFile.setClearButtonEnabled(True)
        self.templateFile.setObjectName("templateFile")
        self.horizontalLayout_4.addWidget(self.templateFile)
        self.toolButtonTemplatePath = QtWidgets.QToolButton(self.groupBox_2)
        self.toolButtonTemplatePath.setMinimumSize(QtCore.QSize(120, 0))
        self.toolButtonTemplatePath.setIcon(icon2)
        self.toolButtonTemplatePath.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toolButtonTemplatePath.setObjectName("toolButtonTemplatePath")
        self.horizontalLayout_4.addWidget(self.toolButtonTemplatePath)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.page1)
        self.page2 = QtWidgets.QWidget()
        self.page2.setObjectName("page2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_vector = QtWidgets.QGroupBox(self.page2)
        self.groupBox_vector.setMinimumSize(QtCore.QSize(0, 110))
        self.groupBox_vector.setObjectName("groupBox_vector")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_vector)
        self.horizontalLayout_6.setSpacing(20)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.groupBox_vector)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.frame = QtWidgets.QFrame(self.groupBox_vector)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.exportTIKZ = QtWidgets.QCheckBox(self.frame)
        self.exportTIKZ.setChecked(True)
        self.exportTIKZ.setObjectName("exportTIKZ")
        self.verticalLayout_5.addWidget(self.exportTIKZ)
        self.exportSVG = QtWidgets.QCheckBox(self.frame)
        self.exportSVG.setObjectName("exportSVG")
        self.verticalLayout_5.addWidget(self.exportSVG)
        self.exportPDF = QtWidgets.QCheckBox(self.frame)
        self.exportPDF.setObjectName("exportPDF")
        self.verticalLayout_5.addWidget(self.exportPDF)
        self.exportPNG = QtWidgets.QCheckBox(self.frame)
        self.exportPNG.setChecked(False)
        self.exportPNG.setObjectName("exportPNG")
        self.verticalLayout_5.addWidget(self.exportPNG)
        self.exportJPEG = QtWidgets.QCheckBox(self.frame)
        self.exportJPEG.setObjectName("exportJPEG")
        self.verticalLayout_5.addWidget(self.exportJPEG)
        self.horizontalLayout_6.addWidget(self.frame)
        self.verticalLayout_3.addWidget(self.groupBox_vector)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum
        )
        self.verticalLayout_3.addItem(spacerItem2)
        self.groupBox_rasterParam = QtWidgets.QGroupBox(self.page2)
        self.groupBox_rasterParam.setMinimumSize(QtCore.QSize(0, 130))
        self.groupBox_rasterParam.setObjectName("groupBox_rasterParam")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_rasterParam)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.labelDPI = QtWidgets.QLabel(self.groupBox_rasterParam)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDPI.sizePolicy().hasHeightForWidth())
        self.labelDPI.setSizePolicy(sizePolicy)
        self.labelDPI.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelDPI.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.labelDPI.setObjectName("labelDPI")
        self.horizontalLayout_8.addWidget(self.labelDPI)
        self.exportDPI = QtWidgets.QSpinBox(self.groupBox_rasterParam)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportDPI.sizePolicy().hasHeightForWidth())
        self.exportDPI.setSizePolicy(sizePolicy)
        self.exportDPI.setFrame(True)
        self.exportDPI.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.exportDPI.setMaximum(3000)
        self.exportDPI.setSingleStep(10)
        self.exportDPI.setProperty("value", 150)
        self.exportDPI.setObjectName("exportDPI")
        self.horizontalLayout_8.addWidget(self.exportDPI)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelQuality = QtWidgets.QLabel(self.groupBox_rasterParam)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelQuality.sizePolicy().hasHeightForWidth())
        self.labelQuality.setSizePolicy(sizePolicy)
        self.labelQuality.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.labelQuality.setObjectName("labelQuality")
        self.horizontalLayout_7.addWidget(self.labelQuality)
        self.exportQuality = QtWidgets.QSpinBox(self.groupBox_rasterParam)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.exportQuality.sizePolicy().hasHeightForWidth()
        )
        self.exportQuality.setSizePolicy(sizePolicy)
        self.exportQuality.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.exportQuality.setMaximum(100)
        self.exportQuality.setProperty("value", 80)
        self.exportQuality.setObjectName("exportQuality")
        self.horizontalLayout_7.addWidget(self.exportQuality)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addWidget(self.groupBox_rasterParam)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.verticalLayout_3.addItem(spacerItem3)
        self.stackedWidget.addWidget(self.page2)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfigDialog)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.labelDPI.setBuddy(self.exportDPI)
        self.labelQuality.setBuddy(self.exportQuality)

        self.retranslateUi(ConfigDialog)
        self.stackedWidget.setCurrentIndex(1)
        self.listWidget.currentRowChanged["int"].connect(
            self.stackedWidget.setCurrentIndex
        )
        self.buttonBox.accepted.connect(ConfigDialog.accept)
        self.buttonBox.rejected.connect(ConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)
        ConfigDialog.setTabOrder(self.listWidget, self.cmPath)
        ConfigDialog.setTabOrder(self.cmPath, self.toolButtonCMPath)
        ConfigDialog.setTabOrder(self.toolButtonCMPath, self.templateFile)
        ConfigDialog.setTabOrder(self.templateFile, self.toolButtonTemplatePath)
        ConfigDialog.setTabOrder(self.toolButtonTemplatePath, self.exportTIKZ)
        ConfigDialog.setTabOrder(self.exportTIKZ, self.exportPDF)
        ConfigDialog.setTabOrder(self.exportPDF, self.exportDPI)
        ConfigDialog.setTabOrder(self.exportDPI, self.exportQuality)

    def retranslateUi(self, ConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfigDialog.setWindowTitle(_translate("ConfigDialog", "Config Dialog"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("ConfigDialog", "General"))
        item = self.listWidget.item(1)
        item.setText(_translate("ConfigDialog", "Exporting"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(
            _translate("ConfigDialog", "Circuit Macros Location", "Group box title")
        )
        self.cmPath.setPlaceholderText(_translate("ConfigDialog", "Enter Path Name"))
        self.toolButtonCMPath.setText(
            _translate("ConfigDialog", "Choose...", "Button text")
        )
        self.groupBox_2.setTitle(
            _translate("ConfigDialog", "LaTeX Template File", "Group box title")
        )
        self.templateFile.setPlaceholderText(
            _translate("ConfigDialog", "Enter Path Name")
        )
        self.toolButtonTemplatePath.setText(
            _translate("ConfigDialog", "Choose...", "Button text")
        )
        self.groupBox_vector.setTitle(
            _translate("ConfigDialog", "Image formats to export", "Group box title")
        )
        self.label_2.setText(
            _translate(
                "ConfigDialog",
                'Choose which formats will be saved when the button "Export" is pressed:',
            )
        )
        self.exportTIKZ.setText(_translate("ConfigDialog", "&TIKZ"))
        self.exportSVG.setText(_translate("ConfigDialog", "SVG"))
        self.exportPDF.setText(_translate("ConfigDialog", "PD&F"))
        self.exportPNG.setText(_translate("ConfigDialog", "&PNG (raster)"))
        self.exportJPEG.setText(_translate("ConfigDialog", "&JPEG (raster)"))
        self.groupBox_rasterParam.setTitle(
            _translate(
                "ConfigDialog", "Raster image export parameters", "Group box title"
            )
        )
        self.labelDPI.setText(
            _translate(
                "ConfigDialog", "Ras&ter image resolution in dots per inch (dpi):"
            )
        )
        self.exportDPI.setSuffix(
            _translate(
                "ConfigDialog", " dpi", "Suffix in spin box (translate to acronym)"
            )
        )
        self.labelQuality.setText(
            _translate(
                "ConfigDialog", "Image &quality for lossy formats like jpeg (percent):"
            )
        )
        self.exportQuality.setSuffix(
            _translate("ConfigDialog", " %", "Spin box suffix")
        )


from pycirkuit.resources import resources_rc


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ConfigDialog = QtWidgets.QDialog()
    ui = Ui_ConfigDialog()
    ui.setupUi(ConfigDialog)
    ConfigDialog.show()
    sys.exit(app.exec_())
