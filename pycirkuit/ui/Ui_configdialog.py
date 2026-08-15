# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QToolButton,
    QVBoxLayout, QWidget)
from pycirkuit.resources import resources_rc

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        if not ConfigDialog.objectName():
            ConfigDialog.setObjectName(u"ConfigDialog")
        ConfigDialog.resize(899, 561)
        ConfigDialog.setMinimumSize(QSize(800, 0))
        self.verticalLayout = QVBoxLayout(ConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = QListWidget(ConfigDialog)
        icon = QIcon()
        icon.addFile(u":/pixmaps/CfgGeneral", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setTextAlignment(Qt.AlignCenter)
        __qlistwidgetitem.setIcon(icon)
        __qlistwidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        icon1 = QIcon()
        icon1.addFile(u":/pixmaps/CfgExportImage", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setTextAlignment(Qt.AlignCenter)
        __qlistwidgetitem1.setIcon(icon1)
        __qlistwidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QSize(128, 16777215))
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setStyleSheet(u"padding-top: 10px; \n"
"background-color: rgb(255, 255, 255);")
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.listWidget.setIconSize(QSize(48, 48))
        self.listWidget.setTextElideMode(Qt.ElideNone)
        self.listWidget.setFlow(QListView.LeftToRight)
        self.listWidget.setProperty(u"isWrapping", True)
        self.listWidget.setSpacing(12)
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setWordWrap(True)

        self.horizontalLayout.addWidget(self.listWidget)

        self.stackedWidget = QStackedWidget(ConfigDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setBaseSize(QSize(0, 0))
        self.stackedWidget.setFrameShape(QFrame.Panel)
        self.stackedWidget.setFrameShadow(QFrame.Raised)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_2 = QVBoxLayout(self.page1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.page1)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 100))
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cmPath = QLineEdit(self.groupBox)
        self.cmPath.setObjectName(u"cmPath")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cmPath.sizePolicy().hasHeightForWidth())
        self.cmPath.setSizePolicy(sizePolicy2)
        self.cmPath.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.cmPath)

        self.toolButtonCMPath = QToolButton(self.groupBox)
        self.toolButtonCMPath.setObjectName(u"toolButtonCMPath")
        self.toolButtonCMPath.setMinimumSize(QSize(120, 0))
        icon2 = QIcon()
        icon2.addFile(u":/icons/Open", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButtonCMPath.setIcon(icon2)
        self.toolButtonCMPath.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_3.addWidget(self.toolButtonCMPath)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer_5 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.groupBox_latexEngine = QGroupBox(self.page1)
        self.groupBox_latexEngine.setObjectName(u"groupBox_latexEngine")
        self.groupBox_latexEngine.setMinimumSize(QSize(0, 70))
        self.groupBox_latexEngine.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_latexEngine = QHBoxLayout(self.groupBox_latexEngine)
        self.horizontalLayout_latexEngine.setObjectName(u"horizontalLayout_latexEngine")
        self.latexEngine = QComboBox(self.groupBox_latexEngine)
        self.latexEngine.setObjectName(u"latexEngine")

        self.horizontalLayout_latexEngine.addWidget(self.latexEngine)


        self.verticalLayout_2.addWidget(self.groupBox_latexEngine)

        self.verticalSpacer_6 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.groupBox_2 = QGroupBox(self.page1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 100))
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.templateFile = QLineEdit(self.groupBox_2)
        self.templateFile.setObjectName(u"templateFile")
        self.templateFile.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.templateFile)

        self.toolButtonTemplatePath = QToolButton(self.groupBox_2)
        self.toolButtonTemplatePath.setObjectName(u"toolButtonTemplatePath")
        self.toolButtonTemplatePath.setMinimumSize(QSize(120, 0))
        self.toolButtonTemplatePath.setIcon(icon2)
        self.toolButtonTemplatePath.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_4.addWidget(self.toolButtonTemplatePath)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_3 = QVBoxLayout(self.page2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_vector = QGroupBox(self.page2)
        self.groupBox_vector.setObjectName(u"groupBox_vector")
        self.groupBox_vector.setMinimumSize(QSize(0, 110))
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_vector)
        self.horizontalLayout_6.setSpacing(20)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(self.groupBox_vector)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.label_2)

        self.frame = QFrame(self.groupBox_vector)
        self.frame.setObjectName(u"frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy4)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.exportTIKZ = QCheckBox(self.frame)
        self.exportTIKZ.setObjectName(u"exportTIKZ")
        self.exportTIKZ.setChecked(True)

        self.verticalLayout_5.addWidget(self.exportTIKZ)

        self.exportSVG = QCheckBox(self.frame)
        self.exportSVG.setObjectName(u"exportSVG")

        self.verticalLayout_5.addWidget(self.exportSVG)

        self.exportPDF = QCheckBox(self.frame)
        self.exportPDF.setObjectName(u"exportPDF")

        self.verticalLayout_5.addWidget(self.exportPDF)

        self.exportPNG = QCheckBox(self.frame)
        self.exportPNG.setObjectName(u"exportPNG")
        self.exportPNG.setChecked(False)

        self.verticalLayout_5.addWidget(self.exportPNG)

        self.exportJPEG = QCheckBox(self.frame)
        self.exportJPEG.setObjectName(u"exportJPEG")

        self.verticalLayout_5.addWidget(self.exportJPEG)


        self.horizontalLayout_6.addWidget(self.frame)


        self.verticalLayout_3.addWidget(self.groupBox_vector)

        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.groupBox_rasterParam = QGroupBox(self.page2)
        self.groupBox_rasterParam.setObjectName(u"groupBox_rasterParam")
        self.groupBox_rasterParam.setMinimumSize(QSize(0, 130))
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_rasterParam)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelDPI = QLabel(self.groupBox_rasterParam)
        self.labelDPI.setObjectName(u"labelDPI")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(5)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.labelDPI.sizePolicy().hasHeightForWidth())
        self.labelDPI.setSizePolicy(sizePolicy5)
        self.labelDPI.setFrameShape(QFrame.NoFrame)
        self.labelDPI.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.labelDPI)

        self.exportDPI = QSpinBox(self.groupBox_rasterParam)
        self.exportDPI.setObjectName(u"exportDPI")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.exportDPI.sizePolicy().hasHeightForWidth())
        self.exportDPI.setSizePolicy(sizePolicy6)
        self.exportDPI.setFrame(True)
        self.exportDPI.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.exportDPI.setMaximum(3000)
        self.exportDPI.setSingleStep(10)
        self.exportDPI.setValue(150)

        self.horizontalLayout_8.addWidget(self.exportDPI)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelQuality = QLabel(self.groupBox_rasterParam)
        self.labelQuality.setObjectName(u"labelQuality")
        sizePolicy5.setHeightForWidth(self.labelQuality.sizePolicy().hasHeightForWidth())
        self.labelQuality.setSizePolicy(sizePolicy5)
        self.labelQuality.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.labelQuality)

        self.exportQuality = QSpinBox(self.groupBox_rasterParam)
        self.exportQuality.setObjectName(u"exportQuality")
        sizePolicy6.setHeightForWidth(self.exportQuality.sizePolicy().hasHeightForWidth())
        self.exportQuality.setSizePolicy(sizePolicy6)
        self.exportQuality.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.exportQuality.setMaximum(100)
        self.exportQuality.setValue(80)

        self.horizontalLayout_7.addWidget(self.exportQuality)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.verticalLayout_3.addWidget(self.groupBox_rasterParam)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page2)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttonBox = QDialogButtonBox(ConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

#if QT_CONFIG(shortcut)
        self.labelDPI.setBuddy(self.exportDPI)
        self.labelQuality.setBuddy(self.exportQuality)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.listWidget, self.cmPath)
        QWidget.setTabOrder(self.cmPath, self.toolButtonCMPath)
        QWidget.setTabOrder(self.toolButtonCMPath, self.latexEngine)
        QWidget.setTabOrder(self.latexEngine, self.templateFile)
        QWidget.setTabOrder(self.templateFile, self.toolButtonTemplatePath)
        QWidget.setTabOrder(self.toolButtonTemplatePath, self.exportTIKZ)
        QWidget.setTabOrder(self.exportTIKZ, self.exportPDF)
        QWidget.setTabOrder(self.exportPDF, self.exportDPI)
        QWidget.setTabOrder(self.exportDPI, self.exportQuality)

        self.retranslateUi(ConfigDialog)
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)
        self.buttonBox.accepted.connect(ConfigDialog.accept)
        self.buttonBox.rejected.connect(ConfigDialog.reject)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(ConfigDialog)
    # setupUi

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QCoreApplication.translate("ConfigDialog", u"Config Dialog", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("ConfigDialog", u"General", None))
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("ConfigDialog", u"Exporting", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("ConfigDialog", u"Circuit Macros Location", u"Group box title"))
        self.cmPath.setPlaceholderText(QCoreApplication.translate("ConfigDialog", u"Enter Path Name", None))
        self.toolButtonCMPath.setText(QCoreApplication.translate("ConfigDialog", u"Choose...", u"Button text"))
        self.groupBox_latexEngine.setTitle(QCoreApplication.translate("ConfigDialog", u"LaTeX Engine", u"Group box title"))
        self.groupBox_2.setTitle(QCoreApplication.translate("ConfigDialog", u"LaTeX Template File", u"Group box title"))
        self.templateFile.setPlaceholderText(QCoreApplication.translate("ConfigDialog", u"Enter Path Name", None))
        self.toolButtonTemplatePath.setText(QCoreApplication.translate("ConfigDialog", u"Choose...", u"Button text"))
        self.groupBox_vector.setTitle(QCoreApplication.translate("ConfigDialog", u"Image formats to export", u"Group box title"))
        self.label_2.setText(QCoreApplication.translate("ConfigDialog", u"Choose which formats will be saved when the button \"Export\" is pressed:", None))
        self.exportTIKZ.setText(QCoreApplication.translate("ConfigDialog", u"&TIKZ", None))
        self.exportSVG.setText(QCoreApplication.translate("ConfigDialog", u"SVG", None))
        self.exportPDF.setText(QCoreApplication.translate("ConfigDialog", u"PD&F", None))
        self.exportPNG.setText(QCoreApplication.translate("ConfigDialog", u"&PNG (raster)", None))
        self.exportJPEG.setText(QCoreApplication.translate("ConfigDialog", u"&JPEG (raster)", None))
        self.groupBox_rasterParam.setTitle(QCoreApplication.translate("ConfigDialog", u"Raster image export parameters", u"Group box title"))
        self.labelDPI.setText(QCoreApplication.translate("ConfigDialog", u"Ras&ter image resolution in dots per inch (dpi):", None))
        self.exportDPI.setSuffix(QCoreApplication.translate("ConfigDialog", u" dpi", u"Suffix in spin box (translate to acronym)"))
        self.labelQuality.setText(QCoreApplication.translate("ConfigDialog", u"Image &quality for lossy formats like jpeg (percent):", None))
        self.exportQuality.setSuffix(QCoreApplication.translate("ConfigDialog", u" %", u"Spin box suffix"))
    # retranslateUi

