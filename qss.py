class NativePythonObject(object):
    def __init__(self, message):
        self.message = message

    def printMessage(self):
        print(self.message)
        sys.exit()

class SignalEmitter(QObject):
    theSignal = pyqtSignal(NativePythonObject)

    def __init__(self, toBeSent, parent=None):
        super(SignalEmitter, self).__init__(parent)
        self.toBeSent = toBeSent

    def emitSignal(self):
        self.theSignal.emit(toBeSent)

class ClassWithSlot(object):
    def __init__(self, signalEmitter):
        self.signalEmitter = signalEmitter
        self.signalEmitter.theSignal.connect(self.theSlot)

    def theSlot(self, ourNativePythonType):
        ourNativePythonType.printMessage()

if __name__ == "__main__":
    toBeSent = NativePythonObject("Hello World")
    signalEmitter = SignalEmitter(toBeSent)
    classWithSlot = ClassWithSlot(signalEmitter)
    signalEmitter.emitSignal()