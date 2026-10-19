import copy
import json
import tempfile
import unittest
from pathlib import Path
from guardar_bitacora import save

class BitacoraTests(unittest.TestCase):
    def capture(self):
        return {'captured_utc':'2026-10-19T22:00:00Z','complete':True,'issues':[
            {'key':'ASTRA-20','owner_is_cristian':True,'summary':'Banco USB',
             'status':'En curso','description':'Prueba de software',
             'comments':[{'id':'1','body':'Resultado inicial','created':'2026-10-17','author':'Cristian'}],
             'changelog':[]}]}

    def test_updates_preserve_original(self):
        with tempfile.TemporaryDirectory() as d:
            c=self.capture();first=save(c,d)
            original=(first/'captura.json').read_bytes()
            c['captured_utc']='2026-10-20T22:00:00Z'
            c['issues'][0]['comments'].append({'id':'2','body':'Actualización con evidencia nueva'})
            second=save(c,d)
            self.assertNotEqual(first,second)
            self.assertEqual((first/'captura.json').read_bytes(),original)
            self.assertEqual(len(list(Path(d).glob('*/manifest.json'))),2)

    def test_incomplete_and_foreign_captures_leave_no_output(self):
        for mutation in ['complete','owner','comments','history','key']:
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as d:
                c=self.capture()
                if mutation=='complete': c['complete']=False
                if mutation=='owner': c['issues'][0]['owner_is_cristian']=False
                if mutation=='comments': c['issues'][0]['comments_complete']=False
                if mutation=='history': c['issues'][0]['changelog_complete']=False
                if mutation=='key': c['issues'][0]['key']='../escape'
                with self.assertRaises(ValueError): save(c,d)
                self.assertEqual(list(Path(d).iterdir()),[])

    def test_same_content_and_sync_notice_do_not_create_loops(self):
        for marker in ['[JIRA-GITHUB-SYNC]',r'\[JIRA-GITHUB-SYNC\]']:
            with self.subTest(marker=marker),tempfile.TemporaryDirectory() as d:
                c=self.capture();save(c,d)
                c['captured_utc']='2026-10-20T22:00:00Z'
                c['issues'][0]['updated']='2026-10-20T22:00:00Z'
                c['issues'][0]['comments'].append({'id':'2','body':marker+' Respaldo publicado'})
                self.assertIsNone(save(c,d))

    def test_restricted_comments_and_contact_metadata_are_not_published(self):
        with tempfile.TemporaryDirectory() as d:
            c=self.capture()
            c['issues'][0]['emailAddress']='private@example.test'
            c['issues'][0]['comments'] += [
                {'id':'2','body':'secreto','visibility':{'type':'role','value':'privado'}},
                {'id':'3','body':'interno','jsdPublic':False},
                {'id':'4','body':'Consultar a private@example.test'}]
            folder=save(c,d)
            text=(folder/'captura.json').read_text(encoding='utf-8')
            self.assertNotIn('private@example.test',text)
            bodies=[c['body'] for c in json.loads(text)['issues'][0]['comments']]
            self.assertNotIn('secreto',bodies)
            self.assertNotIn('interno',bodies)
            self.assertEqual(json.loads(text)['issues'][0]['excluded_comments'],2)

    def test_previous_fingerprint_version_does_not_force_another_capture(self):
        with tempfile.TemporaryDirectory() as d:
            c=self.capture();folder=save(c,d)
            manifest=folder/'manifest.json'
            old=json.loads(manifest.read_text(encoding='utf-8'))
            old['content_sha256']='huella_de_una_regla_anterior'
            manifest.write_text(json.dumps(old),encoding='utf-8')
            self.assertIsNone(save(c,d))

if __name__=='__main__': unittest.main(verbosity=2)
