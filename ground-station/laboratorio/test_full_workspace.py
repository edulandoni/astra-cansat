"""ASTRA-41/22/39: integración Qt completa con transporte/cámaras aislados."""
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication,QAbstractItemView
from qt_app import Laboratory
from runtime import AREA,FIELDS
from telemetry_workspace import SPECS
sys.path.insert(0,str(AREA/'camaras-banco'))
from PIL import Image


class FullWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])
        assert cls.app.platformName()=='offscreen'

    def wait(self,predicate,seconds=4):
        until=time.monotonic()+seconds
        while not predicate() and time.monotonic()<until:self.app.processEvents();time.sleep(.01)
        self.assertTrue(predicate())

    def close(self,w):
        w.close()
        self.wait(lambda:not w.jobs and (not w.source or w.source.closed))
        w.close();self.app.processEvents()

    def test_all_channels_plots_commands_and_destinations(self):
        with tempfile.TemporaryDirectory() as folder,patch('serial.Serial',side_effect=AssertionError('Sin USB')),patch('serial.tools.list_ports.comports',return_value=[]):
            w=Laboratory({'output':folder})
            try:
                self.assertEqual(w.telemetry.variables.rowCount(),22)
                self.assertEqual(len(w.telemetry.plots),11)
                self.assertEqual({k for _,keys in SPECS for k in keys},{'ALTITUDE','PRESSURE','TEMPERATURE','VOLTAGE','CURRENT','GYRO_R','GYRO_P','GYRO_Y','ACCEL_R','ACCEL_P','ACCEL_Y','GPS_ALTITUDE','GPS_SATS','GPS_LATITUDE','GPS_LONGITUDE'})
                self.assertEqual(w.telemetry.count(),7)
                w.backup_path=Path(folder)/'segundo';w.start_source('pc',speed=10)
                self.wait(lambda:w.source.engine.snapshot()['total_valid']>=3)
                w.refresh()
                self.assertTrue(all(len(plot.points)>=3 for plot in w.telemetry.plots))
                self.assertTrue(all(w.telemetry.variables.item(i,1).text()!='—' for i in range(22)))
                self.assertEqual(w.telemetry.storage.rowCount(),4)
                self.assertIn('raw_hex',w.telemetry.raw.toPlainText())
                self.assertIn('ascii',w.telemetry.raw.toPlainText())
                w.telemetry.send('POWER_STATUS')
                self.wait(lambda:any(c['op']=='POWER_STATUS' and c['state']=='executed' for c in w.source.engine.snapshot()['commands']))
                w.refresh();self.assertGreater(w.telemetry.commands.rowCount(),0)
                w.source.engine.disconnected('corte sintético');w.refresh()
                self.assertTrue(all(plot.old for plot in w.telemetry.plots))
                self.assertEqual(w.telemetry.interruptions.rowCount(),1)
                self.assertFalse(w.telemetry.command_buttons['RUN'].isEnabled())
                self.assertIn('Histórica',w.telemetry.variables.item(0,2).text())
                # La misma ventana no puede entregar el puerto activo a una cámara.
                w.source.mode='usb';w.source.port='COM_TEST';w.camera_ports.addItem('Ensayo','COM_TEST');w.camera_ports.setCurrentIndex(1)
                with patch.object(w,'notice') as notice,patch('camera_session.capture',side_effect=AssertionError('Puerto ocupado')):
                    w.capture_camera(1);self.assertIn('telemetría',notice.call_args.args[1])
            finally:self.close(w)

    def test_camera_buttons_unit_sd_identity_and_error(self):
        with tempfile.TemporaryDirectory() as folder,patch('serial.Serial',side_effect=AssertionError('Sin USB')),patch('serial.tools.list_ports.comports',return_value=[]):
            root=Path(folder);registry=root/'registry.json';registry.write_text(json.dumps({'version':1,'cameras':{'camera1':'1111111111111111','camera2':'2222222222222222'}}))
            photo=root/'foto.jpg';Image.new('RGB',(100,80),'green').save(photo)
            w=Laboratory({'output':folder,'camera_registry':str(registry)});w.camera_ports.addItem('Puerto de ensayo','COM_TEST');w.camera_ports.setCurrentIndex(1)
            def capture(unit,identity,port,output,save_sd):
                return dict(photo=photo,operation_ok=True,sd_requested=save_sd,sd_ok=save_sd,finished_utc='2026-10-26T12:00:00+00:00')
            try:
                with patch('camera_session.capture',side_effect=capture) as mocked:
                    for index,unit,sd in [(0,'camera1',False),(1,'camera1',True),(2,'camera2',False),(3,'camera2',True)]:
                        w.camera_action_buttons[index].click();self.wait(lambda:not w.jobs)
                        args=mocked.call_args.args
                        self.assertEqual(args[0],unit);self.assertEqual(args[1],('1' if unit=='camera1' else '2')*16)
                        self.assertEqual(args[2],'COM_TEST');self.assertEqual(args[4],sd)
                        self.assertIn('ESTA SESIÓN',w.photo_badges[1 if unit=='camera1' else 2].text())
                    self.assertIn('2 de 2',w.camera_summary.text())
                with patch('camera_session.capture',side_effect=ValueError('Sin foto nueva')):
                    w.camera_action_buttons[0].click();self.wait(lambda:not w.jobs)
                    self.assertIn('No pude confirmar',w.camera_summary.text())
            finally:self.close(w)

    def test_empirical_archive_unknown_inputs_and_negative_energy(self):
        with tempfile.TemporaryDirectory() as folder,patch('serial.tools.list_ports.comports',return_value=[]):
            w=Laboratory({'output':folder})
            try:
                e=w.experiments;e.calculate_link()
                self.assertEqual(len(e.current_result['missing']),11)
                self.assertIn('TBD',e.link_result.text())
                e.rotor_inputs['efficiency'].setValue(0);e.calculate_rotor()
                self.assertLess(e.current_result['net_incremental_wh'],0)
                self.assertEqual(len(list((w.output/'calculos').glob('*.json'))),2)
                self.assertEqual(e.files.topLevelItemCount(),3)
                self.assertEqual(e.record_table.editTriggers(),QAbstractItemView.NoEditTriggers)
                before=w.radio_table.item(0,1).text();w.cr.setCurrentIndex(3)
                self.assertNotEqual(w.radio_table.item(0,1).text(),before)
                e.run_campaign();self.wait(lambda:not w.jobs,seconds=15)
                self.assertEqual(e.campaign_table.rowCount(),17)
                self.assertIn('6/6',e.campaign_status.text());self.assertIn('11/11',e.campaign_status.text())
                from PySide6.QtWidgets import QTreeWidgetItemIterator
                iterator=QTreeWidgetItemIterator(e.files);paths=[]
                from PySide6.QtCore import Qt
                while iterator.value():
                    name=iterator.value().data(0,Qt.UserRole)
                    if name:paths.append(Path(name))
                    iterator+=1
                expected=[p for folder in ('evidence','config','docs') for p in (AREA/folder).rglob('*') if p.is_file() and p.suffix.lower() in ('.json','.jsonl','.csv','.md','.txt')]
                self.assertEqual(set(paths),set(expected))
            finally:self.close(w)

    def test_qt_sequence_viewer_checks_original_frames(self):
        from test_sequence_verify import fixture
        from qt_sequence import SequenceDialog
        with tempfile.TemporaryDirectory() as folder,patch('serial.Serial',side_effect=AssertionError('Sin USB')):
            root=Path(folder);obj=fixture(root);(root/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            dialog=SequenceDialog(None,root)
            try:
                self.assertEqual(dialog.index,0);self.assertFalse(dialog.picture.pixmap().isNull())
                self.assertIn('1 de 4',dialog.status.text())
                dialog.clock.position=dialog.archive.duration;dialog.refresh()
                self.assertEqual(dialog.index,3)
                (root/'frame_0001.jpg').write_bytes(b'modified')
                dialog.clock.rewind();dialog.refresh();self.assertTrue(dialog.failed)
                self.assertTrue(all(not b.isEnabled() for b in dialog.buttons))
            finally:dialog.close()

    def test_sequence_button_preserves_photo_and_reports_scope(self):
        import threading
        with tempfile.TemporaryDirectory() as folder,patch('serial.tools.list_ports.comports',return_value=[]):
            root=Path(folder);registry=root/'registry.json';registry.write_text(json.dumps({'version':1,'cameras':{'camera1':'1111111111111111','camera2':'2222222222222222'}}))
            w=Laboratory({'output':folder,'camera_registry':str(registry)});w.camera_ports.addItem('Ensayo','COM7');w.camera_ports.setCurrentIndex(1)
            ready=threading.Event()
            def request(*args):
                ready.wait(2);return dict(reported_closed=True,frames=12,path='/test',state='reported_closed')
            try:
                with patch('sequence_session.record',side_effect=request) as mocked:
                    w.sequence_buttons[1].click();w.refresh()
                    self.assertTrue(all(not b.isEnabled() for b in w.camera_action_buttons))
                    self.assertIn('GRABANDO',w.photo_badges[1].text());w.close();self.assertTrue(w.closing)
                    ready.set();self.wait(lambda:not w.jobs)
                    self.assertEqual(mocked.call_args.args[:3],('camera1','1111111111111111','COM7'))
                    self.assertIn('cierre reportado',w.camera_summary.text())
                    self.assertIn('Falta verificar',w.camera_summary.text())
            finally:ready.set();self.close(w)

    def test_video_export_in_dialog_waits_for_result(self):
        from test_sequence_verify import fixture
        from qt_sequence import SequenceDialog
        with tempfile.TemporaryDirectory() as folder,patch('serial.tools.list_ports.comports',return_value=[]):
            root=Path(folder);source=root/'source';source.mkdir();obj=fixture(source)
            (source/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            w=Laboratory({'output':folder});dialog=SequenceDialog(w,source)
            try:
                dialog.start_export(root/'exportados');dialog.close();self.assertTrue(dialog.close_pending)
                self.wait(lambda:not w.jobs,seconds=10)
                self.assertFalse(dialog.exporting);self.assertTrue(dialog.open_export.isEnabled());self.assertIn('MP4 verificado',dialog.export_status.text())
            finally:dialog.close();self.close(w)


if __name__=='__main__':unittest.main()
