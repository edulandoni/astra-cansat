"""ASTRA-41: cierre nativo durante tareas; sin puertos ni hardware."""
import tempfile
import time
import tkinter as tk
import unittest
from app import Laboratory


class Window(tk.Tk):
    closed=False
    def destroy(self):
        self.closed=True
        super().destroy()


class CloseTests(unittest.TestCase):
    def exercise(self, operation):
        with tempfile.TemporaryDirectory() as folder:
            root=Window(); root.withdraw()
            app=Laboratory(root,{'output':folder})
            self.assertEqual(len(app.book.tabs()),8)
            operation(app)
            sim=app.sim
            app.close()
            end=time.monotonic()+10
            while not root.closed and time.monotonic()<end:
                root.update(); time.sleep(.01)
            self.assertTrue(root.closed)
            self.assertFalse(app.recovery_busy)
            if sim:
                self.assertFalse(sim.thread.is_alive())
                self.assertTrue(all(not w.thread.is_alive() for w in sim.store.writers))
                self.assertTrue(all(w['pending']==0 for w in sim.store.status()))

    def test_close_during_recovery(self):self.exercise(lambda app:app.run_recovery())
    def test_close_during_mission(self):self.exercise(lambda app:app.start_sim())

if __name__=='__main__':unittest.main()
