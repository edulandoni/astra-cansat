"""ASTRA-41: liberar widgets de cada prueba antes de destruir QApplication."""
import time
from PySide6.QtCore import QCoreApplication,QEvent
from PySide6.QtWidgets import QApplication
from shiboken6 import isValid


def cleanup_widgets():
    app=QApplication.instance()
    if app is None:return
    if app.platformName()!='offscreen':raise RuntimeError('La limpieza de tests requiere plataforma offscreen.')
    widgets=list(app.topLevelWidgets())
    for w in widgets:
        if isValid(w):w.close()
    until=time.monotonic()+6
    while any(isValid(w) and getattr(w,'jobs',[]) for w in widgets):
        if time.monotonic()>until:raise AssertionError('Quedó un trabajo de interfaz pendiente al terminar el test.')
        app.processEvents();time.sleep(.01)
    for w in widgets:
        if isValid(w):w.deleteLater()
    QCoreApplication.sendPostedEvents(None,QEvent.DeferredDelete)
    app.processEvents()
