# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/orestes/Devel/Software/pycirkuit/pycirkuit/ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(677, 667)
        MainWindow.setMinimumSize(QtCore.QSize(440, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/AppIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setKerning(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_source = QtWidgets.QWidget()
        self.tab_source.setObjectName("tab_source")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_source)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sourceText = pycktTextEditor(self.tab_source)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sourceText.sizePolicy().hasHeightForWidth())
        self.sourceText.setSizePolicy(sizePolicy)
        self.sourceText.setObjectName("sourceText")
        self.horizontalLayout_3.addWidget(self.sourceText)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Text"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_source, icon1, "")
        self.tab_log = QtWidgets.QWidget()
        self.tab_log.setObjectName("tab_log")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_log)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.outputText = QtWidgets.QPlainTextEdit(self.tab_log)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(11)
        self.outputText.setFont(font)
        self.outputText.setReadOnly(True)
        self.outputText.setPlainText("")
        self.outputText.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.outputText.setObjectName("outputText")
        self.horizontalLayout_4.addWidget(self.outputText)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/Output"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_log, icon2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.processButton = QtWidgets.QPushButton(self.centralwidget)
        self.processButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processButton.sizePolicy().hasHeightForWidth())
        self.processButton.setSizePolicy(sizePolicy)
        self.processButton.setBaseSize(QtCore.QSize(0, 0))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Run"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.processButton.setIcon(icon3)
        self.processButton.setObjectName("processButton")
        self.horizontalLayout.addWidget(self.processButton)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.exportTIKZ = QtWidgets.QPushButton(self.centralwidget)
        self.exportTIKZ.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/Export"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportTIKZ.setIcon(icon4)
        self.exportTIKZ.setObjectName("exportTIKZ")
        self.verticalLayout_2.addWidget(self.exportTIKZ)
        self.exportPNG = QtWidgets.QPushButton(self.centralwidget)
        self.exportPNG.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/Bitmap"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportPNG.setIcon(icon5)
        self.exportPNG.setObjectName("exportPNG")
        self.verticalLayout_2.addWidget(self.exportPNG)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 677, 34))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.previewWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.previewWidget.sizePolicy().hasHeightForWidth())
        self.previewWidget.setSizePolicy(sizePolicy)
        self.previewWidget.setMinimumSize(QtCore.QSize(100, 130))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/view-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previewWidget.setWindowIcon(icon6)
        self.previewWidget.setObjectName("previewWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.imageViewer = pycktImageViewer(self.dockWidgetContents)
        self.imageViewer.setAcceptDrops(False)
        self.imageViewer.setAutoFillBackground(True)
        self.imageViewer.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.imageViewer.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.imageViewer.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.imageViewer.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.imageViewer.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
        self.imageViewer.setObjectName("imageViewer")
        self.horizontalLayout_2.addWidget(self.imageViewer)
        self.previewWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.previewWidget)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/Exit"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon7)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/Open"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon8)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/About"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon9)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/Settings"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon10)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/New"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon11)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/Save"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon12)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/SaveAs"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAs.setIcon(icon13)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionCMMan = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/CMman"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCMMan.setIcon(icon14)
        self.actionCMMan.setObjectName("actionCMMan")
        self.actionDpicMan = QtWidgets.QAction(MainWindow)
        self.actionDpicMan.setIcon(icon14)
        self.actionDpicMan.setObjectName("actionDpicMan")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionCMMan)
        self.menuHelp.addAction(self.actionDpicMan)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyCirkuit - by Orestes Mas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_source), _translate("MainWindow", "Source Editor", "Tab title"))
        self.outputText.setPlaceholderText(_translate("MainWindow", "<Empty output>", "Placeholder text"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_log), _translate("MainWindow", "Output Log", "Tab title"))
        self.processButton.setText(_translate("MainWindow", "Process and display", "Button text"))
        self.exportTIKZ.setText(_translate("MainWindow", "Export to TIkZ", "Button text"))
        self.exportPNG.setText(_translate("MainWindow", "Export to PNG"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuHelp.setTitle(_translate("MainWindow", "Hel&p"))
        self.menuSettings.setTitle(_translate("MainWindow", "Setti&ngs"))
        self.previewWidget.setWindowTitle(_translate("MainWindow", "Preview"))
        self.imageViewer.setToolTip(_translate("MainWindow", "<html><head/><body><p>Use:</p>\n"
"<ul>\n"
"<li> Ctrl + Mouse Wheel to Zoom In/Out</li>\n"
"<li> Click and Move to drag the image inside the preview</li>\n"
"</ul>\n"
"</body></html>"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit", "Menu item"))
        self.actionQuit.setStatusTip(_translate("MainWindow", "Close application", "Status Bar Message"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q", "Keyboard Shortcut"))
        self.actionOpen.setText(_translate("MainWindow", "&Open...", "Menu item"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open Drawing"))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Opens an existing drawing", "Status Bar Message"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", "Keyboard Shortcut"))
        self.actionAbout.setText(_translate("MainWindow", "&About PyCirkuit", "Menu item"))
        self.actionAbout.setStatusTip(_translate("MainWindow", "Application information", "Status Bar Message"))
        self.actionPreferences.setText(_translate("MainWindow", "Configure &PyCirkuit...", "Menu item"))
        self.actionPreferences.setStatusTip(_translate("MainWindow", "Opens config dialog", "Status Bar Message"))
        self.actionPreferences.setShortcut(_translate("MainWindow", "Ctrl+P", "Keyboard Shortcut"))
        self.actionNew.setText(_translate("MainWindow", "&New", "Menu item"))
        self.actionNew.setToolTip(_translate("MainWindow", "New Drawing"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Creates an empty drawing", "Status Bar Message"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", "Keyboard Shortcut"))
        self.actionSave.setText(_translate("MainWindow", "&Save", "Menu item"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Saves drawing", "Status Bar Message"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", "Keyboard Shortcut"))
        self.actionSaveAs.setText(_translate("MainWindow", "Sa&ve As...", "Menu item"))
        self.actionSaveAs.setStatusTip(_translate("MainWindow", "Saves drawing with new name", "Status Bar Message"))
        self.actionSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S", "Keyboard Shortcut"))
        self.actionCMMan.setText(_translate("MainWindow", "&Circuit Macros manual"))
        self.actionCMMan.setStatusTip(_translate("MainWindow", "Opens Circuit Macros manual", "Status Bar Message"))
        self.actionCMMan.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionDpicMan.setText(_translate("MainWindow", "&Dpic manual"))
        self.actionDpicMan.setStatusTip(_translate("MainWindow", "Opens Dpic manual", "Status Bar Message"))
        self.actionDpicMan.setShortcut(_translate("MainWindow", "Ctrl+D"))
from pycirkuit.imageviewer import pycktImageViewer
from pycirkuit.texteditor import pycktTextEditor
from pycirkuit.resources import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
