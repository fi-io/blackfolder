
__author__="Leonidus"
__date__ ="$3 Oct, 2010 1:21:42 AM$"

from PyQt4.uic.Compiler.qtproxies import QtGui
import sip
import string
import shutil
import extpathstore
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

#import systray_rc


class DropArea(QtGui.QLabel):

    changed = QtCore.pyqtSignal(QtCore.QMimeData)

    def __init__(self, parent = None):
        super(DropArea, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QtGui.QFrame.Sunken | QtGui.QFrame.StyledPanel)
        
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.clearThis()

    def dragEnterEvent(self, event):
        self.setText("<drop it please!>")
        self.setBackgroundRole(QtGui.QPalette.Mid)
        event.acceptProposedAction()
        self.changed.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasImage():
            self.setPixmap(QtGui.QPixmap(mimeData.imageData()))
        elif mimeData.hasHtml():
            self.setText(mimeData.html())
            self.setTextFormat(QtCore.Qt.RichText)
        elif mimeData.hasText():
            self.setText(mimeData.text())
            self.setTextFormat(QtCore.Qt.PlainText)
        elif mimeData.hasUrls():
            self.setText("\n".join([url.path() for url in mimeData.urls()]))
        else:
            self.setText("Cannot display data")

        self.setBackgroundRole(QtGui.QPalette.Dark)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.clearThis()
        event.accept()

    def clearThis(self):
        self.setText("<drop files>")
        self.setBackgroundRole(QtGui.QPalette.Shadow)
        self.changed.emit(None)


class prefDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(prefDialog, self).__init__(parent)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(AddModTab(), "Add/Modify Ext")
        tabWidget.addTab(AllExtTab(), "View All")
        tabWidget.addTab(AllTran(),"History of Operations")
        tabWidget.addTab(searchFile(),"Search Files")
        tabWidget.addTab(help(),"Help")

        self.cancelButton = QtGui.QPushButton("Close")
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(self.cancelButton, QtGui.QDialogButtonBox.RejectRole)

        self.cancelButton.clicked.connect(self.close)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.setWindowTitle("Black Folder settings")
        self.setMinimumSize(450, 200)

class help(QtGui.QWidget):
    def __init__(self,parent=None):
        super(help,self).__init__(parent)
        self.helpLabel = QtGui.QLabel("           CREDITS\n\n"
                                        "----------------------------\n\n"
                                       "This is the mini project of \n"+
                                       "BRIJ MOHAN LAL SRIVASTAVA \n"
                                       "Final year-IT \n"
                                       "011115022 \n"
                                       "email- contactbrijmohan@gmail.com")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.helpLabel)
        self.setLayout(layout)


class AddModTab(QtGui.QWidget):
    def __init__(self,parent=None):
        super(AddModTab,self).__init__(parent)
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.directoryLabel = QtGui.QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QtGui.QPushButton("Click to select a destination Folder")
        self.extLabel = QtGui.QLabel("Ext:")
        self.statusLabel = QtGui.QLabel("")
        self.extName = QtGui.QLineEdit()

        self.saveButton = QtGui.QPushButton("Save")

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(self.saveButton, QtGui.QDialogButtonBox.ActionRole)

        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.saveButton.clicked.connect(self.addMExt)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.directoryButton)
        layout.addWidget(self.directoryLabel)
        layout.addWidget(self.extLabel)
        layout.addWidget(self.extName)
        layout.addWidget(self.buttonBox)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def setExistingDirectory(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,"QFileDialog.getExistingDirectory()",
                self.directoryLabel.text(), options)
        if directory:
            self.directoryLabel.setText(directory)

    def addMExt(self):
        if self.extName.text() != "" and self.directoryLabel.text()!= "":
            if extpathstore.chDict(str(self.extName.text().upper()), str(self.directoryLabel.text())) == 1:
                self.statusLabel.setText("Dir for "+self.extName.text()+" modified")
            else:
                self.statusLabel.setText("New ext "+self.extName.text()+" added for "+self.directoryLabel.text())
        else:
            self.statusLabel.setText("Both fields are needed !")
        
class AllExtTab(QtGui.QWidget):
    def __init__(self,parent=None):
        super(AllExtTab,self).__init__(parent)

        self.refreshButton = QtGui.QPushButton("Refresh")
        self.rbuttonBox = QtGui.QDialogButtonBox()
        self.rbuttonBox.addButton(self.refreshButton, QtGui.QDialogButtonBox.ActionRole)
        self.refreshButton.pressed.connect(self.FillExtTable)

        self.ExtTable = QtGui.QTableWidget()
        self.ExtTable.setColumnCount(2)
        self.ExtTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ExtTable.setHorizontalHeaderLabels(["Extension","Directory"])
        self.ExtTable.horizontalHeader().setStretchLastSection(True)

        self.FillExtTable()

        TLayout = QtGui.QVBoxLayout()
        TLayout.addWidget(self.ExtTable)
        TLayout.addWidget(self.rbuttonBox)
        self.setLayout(TLayout)

    def FillExtTable(self):
        self.ExtTable.setRowCount(0)

        for key in extpathstore.epaths:
            row = self.ExtTable.rowCount()
            self.ExtTable.insertRow(row)
            self.ExtTable.setItem(row, 0, QtGui.QTableWidgetItem(key))
            self.ExtTable.setItem(row, 1, QtGui.QTableWidgetItem(extpathstore.epaths[key]))
            
        self.ExtTable.resizeColumnToContents(4)

class AllTran(QtGui.QWidget):
    def __init__(self,parent=None):
        super(AllTran,self).__init__(parent)
        self.refreshButton = QtGui.QPushButton("Refresh")
        self.rbuttonBox = QtGui.QDialogButtonBox()
        self.rbuttonBox.addButton(self.refreshButton, QtGui.QDialogButtonBox.ActionRole)
        self.refreshButton.pressed.connect(self.FillTranTable)

        self.TranTable = QtGui.QTableWidget()
        self.TranTable.setColumnCount(2)
        self.TranTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TranTable.setHorizontalHeaderLabels(["Original File","Moved to"])
        self.TranTable.horizontalHeader().setStretchLastSection(True)

        self.FillTranTable()

        TrLayout = QtGui.QVBoxLayout()
        TrLayout.addWidget(self.TranTable)
        TrLayout.addWidget(self.rbuttonBox)
        self.setLayout(TrLayout)

    def FillTranTable(self):
        self.TranTable.setRowCount(0)

        for key in extpathstore.tran:
            row = self.TranTable.rowCount()
            self.TranTable.insertRow(row)
            self.TranTable.setItem(row, 0, QtGui.QTableWidgetItem(key))
            self.TranTable.setItem(row, 1, QtGui.QTableWidgetItem(extpathstore.tran[key]))

        self.TranTable.resizeColumnToContents(4)

class searchFile(QtGui.QWidget):
    def __init__(self,parent=None):
        super(searchFile,self).__init__(parent)
        
        self.searchLabel = QtGui.QLabel("Enter search string with extension:")
        self.searchName = QtGui.QLineEdit()
        self.DirName = QtGui.QLineEdit()
        self.searchButton = QtGui.QPushButton("Search")

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)

        self.searchButton.clicked.connect(self.searchInDB)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.searchLabel)
        layout.addWidget(self.searchName)
        layout.addWidget(self.buttonBox)
        layout.addWidget(self.DirName)
        self.setLayout(layout)

    def searchInDB(self):
        self.DirName.setText(extpathstore.searchThis(str(self.searchName.text())))

class DropSiteWindow(QtGui.QWidget):

    def __init__(self):
        super(DropSiteWindow, self).__init__()

        #Tray icon initialization
        self.createActions()
        self.createTrayIcon()

        #Progress bar initialization
        self.pbar = QtGui.QProgressBar()

        self.dropArea = DropArea()
        self.dropArea.changed.connect(self.updateFormatsTable)

        #show/hide details table
        self.showIconCheckBox = QtGui.QCheckBox("Show Details")
        self.showIconCheckBox.setChecked(False)

        self.formatsTable = QtGui.QTableWidget()
        self.formatsTable.setColumnCount(3)
        self.formatsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.formatsTable.setHorizontalHeaderLabels(["Dropped File(s)","File Type", "Moved to..."])
        self.formatsTable.horizontalHeader().setStretchLastSection(True)

        #triggering table show/hide operations
        self.showIconCheckBox.toggle()
        self.connect(self.showIconCheckBox, QtCore.SIGNAL('stateChanged(int)'), self.toggleTable)


        self.clearButton = QtGui.QPushButton("Clear")
        self.quitButton = QtGui.QPushButton("Hide")
        self.prefButton = QtGui.QPushButton("Options")

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.addButton(self.clearButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        self.buttonBox.addButton(self.prefButton, QtGui.QDialogButtonBox.ActionRole)

        self.quitButton.pressed.connect(self.close)
        self.clearButton.pressed.connect(self.clear)
        self.prefButton.pressed.connect(self.addModifyExt)

        mainLayout = QtGui.QVBoxLayout()
#        mainLayout.addWidget(self.abstractLabel)
        mainLayout.addWidget(self.dropArea)
        mainLayout.addWidget(self.pbar)
        mainLayout.addWidget(self.showIconCheckBox)
        mainLayout.addWidget(self.formatsTable)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.trayIcon.show()

        self.setWindowTitle("Black Folder")
        self.setMinimumSize(350, 300)

    def toggleTable(self, value):
        if self.showIconCheckBox.isChecked():
            self.formatsTable.show()
            self.resize(350, 500)
        else:
            self.formatsTable.hide()
            self.resize(350,200)

    def clear(self):
        self.dropArea.setText("<drop files>")
        self.dropArea.setBackgroundRole(QtGui.QPalette.Shadow)
        self.pbar.setValue(0)
        self.dropArea.changed.emit(None)

    def addModifyExt(self):
        self.pref = prefDialog()
        self.pref.show()


    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            self.hide()
            event.ignore()
            self.showMessage()

    def showMessage(self):
        icon = QtGui.QSystemTrayIcon.MessageIcon(1)
        self.trayIcon.showMessage("Black Folder",
                "Quitting Black-Folder directly can harm running file operations.It is still running in background.You can Right-click on this icon and do other operations.", icon,
                15 * 1000)

    def createActions(self):
        self.minimizeAction = QtGui.QAction("Mi&nimize", self,
                triggered=self.hide)

        self.maximizeAction = QtGui.QAction("Ma&ximize", self,
                triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self,
                triggered=self.showNormal)

        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addAction(self.minimizeAction)
         self.trayIconMenu.addAction(self.maximizeAction)
         self.trayIconMenu.addAction(self.restoreAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)

         self.trayIcon.setIcon(QtGui.QIcon('folder.ico'))
         self.setWindowIcon(QtGui.QIcon('folder.ico'))


    def updateFormatsTable(self, mimeData=None):
        self.formatsTable.setRowCount(0)
        self.errorMessageDialog = QtGui.QErrorMessage(self)
        self.step = 0;

        if mimeData is None:
            return

        for format in mimeData.formats():
            formatItem = QtGui.QTableWidgetItem(format)
            formatItem.setFlags(QtCore.Qt.ItemIsEnabled)
            formatItem.setTextAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            
            if format=='text/uri-list':
                pbarInc = 100/len(mimeData.urls())
                pbarVal = 0
                fctr = 0
                for url in mimeData.urls():
                    text = url.toLocalFile()
                    #print os.getcwd()
                    fctr = fctr + 1
                    pbarVal = pbarVal + pbarInc
                    indofdot=string.find(text, '.')
                    if indofdot==-1:
                        type = "Unknown File or Folder"
                    else:
                        type = text[indofdot+1:].upper()


                    fn_len = len(text)
                    while fn_len>0:
                        if text[fn_len-1]=='/':
                            break
                        else:
                            fn_len=fn_len-1

                    #print(text[:fn_len-1]+'/')
                    destpath = extpathstore.findPath(str(type),str(text[:fn_len-1]))
                    extpathstore.originalPath(str(text),str(destpath))
                    extpathstore.forSearch(str(text[fn_len:]), str(destpath))
                            
                    row = self.formatsTable.rowCount()
                    self.formatsTable.insertRow(row)
                    self.formatsTable.setItem(row, 0, QtGui.QTableWidgetItem(text[fn_len:]))
                    self.formatsTable.setItem(row, 1, QtGui.QTableWidgetItem(type+' FILE'))
                    self.formatsTable.setItem(row, 2, QtGui.QTableWidgetItem(destpath))
                    try:
                        shutil.move(text, destpath)
                        if fctr == len(mimeData.urls()):
                            self.pbar.setValue(100)
                        else:
                            self.pbar.setValue(pbarVal)
                    except:
                        self.errorMessageDialog.showMessage(self.tr(
                                    "-An error occured while moving the files."
                                    "-Please check the User Permissions or"
                                    "the existence of destination folder."
                                    "-The File can also be an unrecognised format"
                                    "-OR the source & destination folder are same."))
        self.formatsTable.resizeColumnToContents(4)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    window = DropSiteWindow()
    window.show()
    sys.exit(app.exec_())
    