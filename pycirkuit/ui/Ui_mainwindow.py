# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QDockWidget,
    QGraphicsView,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pycirkuit.imageviewer import pycktImageViewer
from pycirkuit.texteditor import pycktTextEditor
from pycirkuit.resources import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(677, 667)
        MainWindow.setMinimumSize(QSize(440, 400))
        icon = QIcon()
        icon.addFile(":/icons/AppIcon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        icon1 = QIcon()
        icon1.addFile(":/icons/Exit", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionQuit.setIcon(icon1)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        icon2 = QIcon()
        icon2.addFile(":/icons/Open", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionOpen.setIcon(icon2)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        icon3 = QIcon()
        icon3.addFile(":/icons/About", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAbout.setIcon(icon3)
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        icon4 = QIcon()
        icon4.addFile(":/icons/Settings", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionPreferences.setIcon(icon4)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        icon5 = QIcon()
        icon5.addFile(":/icons/New", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionNew.setIcon(icon5)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        icon6 = QIcon()
        icon6.addFile(":/icons/Save", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSave.setIcon(icon6)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        icon7 = QIcon()
        icon7.addFile(":/icons/SaveAs", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSaveAs.setIcon(icon7)
        self.actionCMMan = QAction(MainWindow)
        self.actionCMMan.setObjectName("actionCMMan")
        icon8 = QIcon()
        icon8.addFile(":/icons/CMman", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionCMMan.setIcon(icon8)
        self.actionDpicMan = QAction(MainWindow)
        self.actionDpicMan.setObjectName("actionDpicMan")
        self.actionDpicMan.setIcon(icon8)
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        icon9 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditUndo))
        self.actionUndo.setIcon(icon9)
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        icon10 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditRedo))
        self.actionRedo.setIcon(icon10)
        self.actionToggleComment = QAction(MainWindow)
        self.actionToggleComment.setObjectName("actionToggleComment")
        self.actionFind = QAction(MainWindow)
        self.actionFind.setObjectName("actionFind")
        icon11 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.actionFind.setIcon(icon11)
        self.actionReplace = QAction(MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionCut = QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        icon12 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCut))
        self.actionCut.setIcon(icon12)
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        icon13 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditPaste))
        self.actionPaste.setIcon(icon13)
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        icon14 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCopy))
        self.actionCopy.setIcon(icon14)
        self.actionFindNext = QAction(MainWindow)
        self.actionFindNext.setObjectName("actionFindNext")
        icon15 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.actionFindNext.setIcon(icon15)
        self.actionFindPrevious = QAction(MainWindow)
        self.actionFindPrevious.setObjectName("actionFindPrevious")
        icon16 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.actionFindPrevious.setIcon(icon16)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        font = QFont()
        font.setKerning(True)
        self.tabWidget.setFont(font)
        self.tab_source = QWidget()
        self.tab_source.setObjectName("tab_source")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_source)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sourceText = pycktTextEditor(self.tab_source)
        self.sourceText.setObjectName("sourceText")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sourceText.sizePolicy().hasHeightForWidth())
        self.sourceText.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.sourceText)

        icon17 = QIcon()
        icon17.addFile(":/icons/Text", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tab_source, icon17, "")
        self.tab_log = QWidget()
        self.tab_log.setObjectName("tab_log")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_log)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.outputText = QPlainTextEdit(self.tab_log)
        self.outputText.setObjectName("outputText")
        font1 = QFont()
        font1.setFamilies(["Monospace"])
        font1.setPointSize(11)
        font1.setKerning(True)
        self.outputText.setFont(font1)
        self.outputText.setReadOnly(True)
        self.outputText.setPlainText("")
        self.outputText.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard
            | Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.horizontalLayout_4.addWidget(self.outputText)

        icon18 = QIcon()
        icon18.addFile(":/icons/Output", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tab_log, icon18, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.processButton = QPushButton(self.centralwidget)
        self.processButton.setObjectName("processButton")
        self.processButton.setEnabled(False)
        icon19 = QIcon()
        icon19.addFile(":/icons/Run", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.processButton.setIcon(icon19)

        self.horizontalLayout.addWidget(self.processButton)

        self.exportButton = QPushButton(self.centralwidget)
        self.exportButton.setObjectName("exportButton")
        self.exportButton.setEnabled(False)
        icon20 = QIcon()
        icon20.addFile(":/icons/Export", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportButton.setIcon(icon20)

        self.horizontalLayout.addWidget(self.exportButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 677, 34))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.previewWidget = QDockWidget(MainWindow)
        self.previewWidget.setObjectName("previewWidget")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(
            self.previewWidget.sizePolicy().hasHeightForWidth()
        )
        self.previewWidget.setSizePolicy(sizePolicy1)
        self.previewWidget.setMinimumSize(QSize(100, 130))
        icon21 = QIcon()
        icon21.addFile(
            ":/icons/view-preview.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.previewWidget.setWindowIcon(icon21)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.dockWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.dockWidgetContents.setSizePolicy(sizePolicy2)
        self.horizontalLayout_2 = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.imageViewer = pycktImageViewer(self.dockWidgetContents)
        self.imageViewer.setObjectName("imageViewer")
        self.imageViewer.setAcceptDrops(False)
        self.imageViewer.setAutoFillBackground(True)
        self.imageViewer.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.imageViewer.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.imageViewer.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.imageViewer.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.imageViewer.setRubberBandSelectionMode(
            Qt.ItemSelectionMode.IntersectsItemShape
        )

        self.horizontalLayout_2.addWidget(self.imageViewer)

        self.previewWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(
            Qt.DockWidgetArea.TopDockWidgetArea, self.previewWidget
        )

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
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
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionToggleComment)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addAction(self.actionFindNext)
        self.menuEdit.addAction(self.actionFindPrevious)

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "PyCirkuit - by Orestes Mas", None)
        )
        self.actionQuit.setText(
            QCoreApplication.translate("MainWindow", "&Quit", "Menu item")
        )
        # if QT_CONFIG(statustip)
        self.actionQuit.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Close application", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Q", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(
            QCoreApplication.translate("MainWindow", "&Open...", "Menu item")
        )
        # if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(
            QCoreApplication.translate("MainWindow", "Open Drawing", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.actionOpen.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Opens an existing drawing", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+O", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "&About PyCirkuit", "Menu item")
        )
        # if QT_CONFIG(statustip)
        self.actionAbout.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Application information", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        self.actionPreferences.setText(
            QCoreApplication.translate(
                "MainWindow", "Configure &PyCirkuit...", "Menu item"
            )
        )
        # if QT_CONFIG(statustip)
        self.actionPreferences.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Opens config dialog", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionPreferences.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+P", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionNew.setText(
            QCoreApplication.translate("MainWindow", "&New", "Menu item")
        )
        # if QT_CONFIG(tooltip)
        self.actionNew.setToolTip(
            QCoreApplication.translate("MainWindow", "New Drawing", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.actionNew.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Creates an empty drawing", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+N", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSave.setText(
            QCoreApplication.translate("MainWindow", "&Save", "Menu item")
        )
        # if QT_CONFIG(statustip)
        self.actionSave.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Saves drawing", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+S", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSaveAs.setText(
            QCoreApplication.translate("MainWindow", "Sa&ve As...", "Menu item")
        )
        # if QT_CONFIG(statustip)
        self.actionSaveAs.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Saves drawing with new name", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionSaveAs.setShortcut(
            QCoreApplication.translate(
                "MainWindow", "Ctrl+Shift+S", "Keyboard Shortcut"
            )
        )
        # endif // QT_CONFIG(shortcut)
        self.actionCMMan.setText(
            QCoreApplication.translate("MainWindow", "&Circuit Macros manual", None)
        )
        # if QT_CONFIG(statustip)
        self.actionCMMan.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Opens Circuit Macros manual", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionCMMan.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+M", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionDpicMan.setText(
            QCoreApplication.translate("MainWindow", "&Dpic manual", None)
        )
        # if QT_CONFIG(statustip)
        self.actionDpicMan.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Opens Dpic manual", "Status Bar Message"
            )
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionDpicMan.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+D", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", "&Undo", None))
        # if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Z", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", "&Redo", None))
        # if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Y", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionToggleComment.setText(
            QCoreApplication.translate("MainWindow", "&Toggle Comment", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionToggleComment.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                "Ctrl+/",
                "Keyboard Shortcut is handled by the editor itself, see texteditor.py, so that Shift is tolerated as incidental on ES/CAT keyboard layouts where '/' is typed as Shift+7",
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionFind.setText(
            QCoreApplication.translate("MainWindow", "&Find...", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionFind.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+F", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionReplace.setText(
            QCoreApplication.translate("MainWindow", "&Replace...", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionReplace.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+H", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.actionCut.setText(QCoreApplication.translate("MainWindow", "&Cut", None))
        # if QT_CONFIG(shortcut)
        self.actionCut.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+X", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionPaste.setText(
            QCoreApplication.translate("MainWindow", "&Paste", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionPaste.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+V", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", "C&opy", None))
        # if QT_CONFIG(shortcut)
        self.actionCopy.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+C", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionFindNext.setText(
            QCoreApplication.translate("MainWindow", "Find &Next", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionFindNext.setShortcut(
            QCoreApplication.translate("MainWindow", "F3", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionFindPrevious.setText(
            QCoreApplication.translate("MainWindow", "Find Pre&vious", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionFindPrevious.setShortcut(
            QCoreApplication.translate("MainWindow", "Shift+F3", "Keyboard Shortcut")
        )
        # endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_source),
            QCoreApplication.translate("MainWindow", "Source Editor", "Tab title"),
        )
        self.outputText.setPlaceholderText(
            QCoreApplication.translate(
                "MainWindow", "<Empty output>", "Placeholder text"
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_log),
            QCoreApplication.translate("MainWindow", "Output Log", "Tab title"),
        )
        self.processButton.setText(
            QCoreApplication.translate(
                "MainWindow", "&Process and display", "Button text"
            )
        )
        # if QT_CONFIG(shortcut)
        self.processButton.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+P", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.exportButton.setText(
            QCoreApplication.translate("MainWindow", "E&xport", "Button text")
        )
        # if QT_CONFIG(shortcut)
        self.exportButton.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+X", None)
        )
        # endif // QT_CONFIG(shortcut)
        # if QT_CONFIG(whatsthis)
        self.menuFile.setWhatsThis("")
        # endif // QT_CONFIG(whatsthis)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "Fi&le", None))
        # if QT_CONFIG(whatsthis)
        self.menuHelp.setWhatsThis("")
        # endif // QT_CONFIG(whatsthis)
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Hel&p", None))
        # if QT_CONFIG(whatsthis)
        self.menuSettings.setWhatsThis("")
        # endif // QT_CONFIG(whatsthis)
        self.menuSettings.setTitle(
            QCoreApplication.translate("MainWindow", "Setti&ngs", None)
        )
        # if QT_CONFIG(whatsthis)
        self.menuEdit.setWhatsThis("")
        # endif // QT_CONFIG(whatsthis)
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", "&Edit", None))
        self.previewWidget.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", "Preview", "A window title, NOT an action."
            )
        )
        # if QT_CONFIG(tooltip)
        self.imageViewer.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                "<html><head/><body><p>Use:</p>\n"
                "<ul>\n"
                "<li> Ctrl + Mouse Wheel to Zoom In/Out</li>\n"
                "<li> Click and Move to drag the image inside the preview</li>\n"
                "</ul>\n"
                "</body></html>",
                None,
            )
        )


# endif // QT_CONFIG(tooltip)
# retranslateUi
