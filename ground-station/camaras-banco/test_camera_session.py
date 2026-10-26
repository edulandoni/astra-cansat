"""ASTRA-39: identidad, conservación y resultados independientes del doble chequeo."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from camera_check import ProtocolError
from camera_session import Round, capture, read_evidence, read_registry
from test_camera_check import fixture, DEVICE


def evidence(folder, sd=True):
    folder.mkdir(parents=True)
    info, frame, payload, _ = fixture()
    frame.pop('payload', None)
    frame['sd_status'] = 'READBACK_OK' if sd else 'MOUNT_FAILED'
    frame['saved'] = sd
    result = {'info': info, 'frame': frame, 'request_id': frame['id'],
              'finished_utc': '2026-10-26T04:00:00+00:00', 'sd_requested': True,
              'validation': {'sha256': hashlib.sha256(payload).hexdigest()}}
    (folder / 'foto.jpg').write_bytes(payload)
    (folder / 'resultado.json').write_text(json.dumps(result), encoding='utf-8')
    return result


class SessionTests(unittest.TestCase):
    def test_boot_failure_preserves_explanation_instead_of_missing_info_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / 'resultado.json').write_text(json.dumps({'result': 'incomplete', 'error': 'La placa está en modo programación; hace falta un arranque normal.'}))
            with self.assertRaisesRegex(ProtocolError, 'modo programación'):
                read_evidence(folder, DEVICE)

    def test_distinct_registry_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'registry.json'
            path.write_text(json.dumps({'version': 1, 'cameras': {'camera1': DEVICE, 'camera2': DEVICE.upper()}}))
            with self.assertRaisesRegex(ValueError, 'distintas'):
                read_registry(path)
            path.write_text(json.dumps({'version': 1, 'cameras': {'camera1': DEVICE, 'camera2': '0000000000000022'}}))
            self.assertEqual(len(read_registry(path)), 2)

    def test_saved_photo_rechecked_not_trusted_from_cached_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'capture'; evidence(folder)
            self.assertTrue(read_evidence(folder, DEVICE)['sd_ok'])
            photo = folder / 'foto.jpg'
            photo.write_bytes(photo.read_bytes()[:-10])
            with self.assertRaisesRegex(ProtocolError, 'no coincide'):
                read_evidence(folder, DEVICE)

    def test_wrong_unit_and_wrong_request_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'capture'; result = evidence(folder)
            with self.assertRaisesRegex(ProtocolError, 'otra cámara'):
                read_evidence(folder, '0000000000000022')
            result['request_id'] = '9999999999999999'
            (folder / 'resultado.json').write_text(json.dumps(result))
            with self.assertRaisesRegex(ProtocolError, 'pedido'):
                read_evidence(folder, DEVICE)

    def test_sd_failure_keeps_valid_photo_without_approving_operation(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls = []
            def runner(args, **kwargs):
                calls.append(args)
                out = Path(args[args.index('--output') + 1])
                evidence(out / 'result', sd=False)
                return SimpleNamespace(returncode=1)
            result = capture('camera1', DEVICE, 'COM7', tmp, True, runner=runner)
            self.assertFalse(result['operation_ok'])
            self.assertFalse(result['sd_ok'])
            self.assertTrue(Path(result['photo']).exists())
            self.assertEqual(len(calls), 1)
            self.assertIn('--expect-device', calls[0])
            self.assertNotIn('--reset-once', calls[0])

    def test_missing_result_never_retries_and_diagnostics_are_conserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls = []
            def runner(args, **kwargs):
                calls.append(args)
                kwargs['stderr'].write(b'port in use')
                return SimpleNamespace(returncode=1)
            with self.assertRaisesRegex(ProtocolError, 'resultado único'):
                capture('camera1', DEVICE, 'COM7', tmp, True, runner=runner)
            self.assertEqual(len(calls), 1)
            self.assertEqual(next(Path(tmp).glob('*/diagnostico.txt')).read_bytes(), b'port in use')

    def test_one_failure_cannot_approve_two_cameras_and_rounds_do_not_reuse_success(self):
        state = Round()
        first = {'operation_ok': True, 'sd_ok': True, 'photo': 'previous-photo'}
        state.start('camera1'); state.finish('camera1', first)
        state.start('camera2'); state.finish('camera2', {'operation_ok': False})
        self.assertIn('1 de 2', state.summary())
        state.new()
        self.assertIn('0 de 2', state.summary())
        self.assertIs(state.photos['camera1'], first)
        self.assertNotIn('camera1', state.results)
        state.start('camera1'); state.finish('camera1', {'operation_ok': False})
        self.assertIs(state.photos['camera1'], first)
        self.assertIn('0 de 2', state.summary())

    def test_single_operation_owner_and_wrong_camera_result_rejected(self):
        state = Round(); state.start('camera1')
        with self.assertRaises(ValueError): state.start('camera2')
        with self.assertRaises(ValueError): state.new()
        with self.assertRaises(ValueError): state.finish('camera2', {})
        self.assertEqual(state.busy, 'camera1')


if __name__ == '__main__':
    unittest.main()
