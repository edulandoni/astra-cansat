"""Conservo capturas completas de mis tareas sin sobrescribir el historial."""
import argparse
import hashlib
import json
import re
from pathlib import Path

SITE = 'https://astrateam2026.atlassian.net'
SYNC_MARKER = '[JIRA-GITHUB-SYNC]'

def public_text(value):
    if value is None:
        return ''
    if not isinstance(value, str):
        raise ValueError('Los textos deben llegar en el formato devuelto por el conector.')
    value = re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '[correo omitido en copia pública]', value)
    return re.sub(r'\b\d{6}:[0-9a-f-]{36}\b', '[identificador de cuenta omitido]', value)

def normalize(capture):
    if capture.get('complete') is not True or not capture.get('issues'):
        raise ValueError('No publico una captura vacía o incompleta.')
    issues, keys = [], set()
    for issue in capture['issues']:
        key = issue['key']
        if not re.fullmatch(r'ASTRA-[1-9][0-9]*', key) or key in keys:
            raise ValueError('Clave inválida o duplicada.')
        keys.add(key)
        if issue.get('owner_is_cristian') is not True:
            raise ValueError('Falta verificar creador o asignación antes de exportar.')
        if not issue.get('comments_complete', True) or not issue.get('changelog_complete', True):
            raise ValueError('Faltan páginas de comentarios o historial.')
        row = {name: public_text(issue.get(name)) for name in
               ['summary','description','status','assignee','creator','updated']}
        row.update(key=key, url=f'{SITE}/browse/{key}', owner_is_cristian=True,
                   comments_complete=True, changelog_complete=True)
        row['comments'] = []
        excluded = issue.get('excluded_comments', 0)
        for c in issue.get('comments', []):
            if c.get('visibility') or c.get('jsdPublic') is False:
                excluded += 1
                continue
            ident = str(c['id'])
            if not ident.isdigit():
                raise ValueError('ID de comentario inválido.')
            row['comments'].append({
                **{name: public_text(c.get(name)) for name in ['author','created','updated','body']},
                'id':ident, 'url':f'{SITE}/browse/{key}?focusedCommentId={ident}'})
        row['excluded_comments'] = excluded
        row['changelog'] = []
        for e in issue.get('changelog', []):
            row['changelog'].append({
                **{name:public_text(e.get(name)) for name in ['id','author','created']},
                'items':[{name:public_text(it.get(name)) for name in
                          ['field','fromString','toString']} for it in e.get('items',[])]})
        issues.append(row)
    return sorted(issues, key=lambda x:int(x['key'].split('-')[1]))

def content_hash(issues):
    # Los avisos del propio respaldo no disparan una exportación nueva cada día.
    semantic=json.loads(json.dumps(issues))
    for row in semantic:
        row.pop('updated',None)
        row['comments']=[c for c in row['comments'] if SYNC_MARKER not in
                         c['body'].replace('\\[','[').replace('\\]',']')]
    return hashlib.sha256(json.dumps(semantic,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def save(capture, output):
    issues=normalize(capture)
    fingerprint=content_hash(issues)
    output=Path(output)
    for manifest in sorted(output.glob('*/manifest.json'), reverse=True):
        old_capture=json.loads((manifest.parent/'captura.json').read_text(encoding='utf-8'))
        # Recalculo la comparación con la regla actual; el manifest histórico queda intacto.
        if content_hash(old_capture['issues'])==fingerprint:
            return None
        break
    stamp=str(capture['captured_utc'])
    # La fecha proviene de la consulta real, no de las fechas históricas de Jira.
    if not re.match(r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}',stamp):
        raise ValueError('Falta una fecha UTC de captura válida.')
    folder=output/(re.sub(r'[^0-9A-Za-z_-]','-',stamp)+'_'+fingerprint[:12])
    folder.mkdir(parents=True,exist_ok=False)
    record={'captured_utc':stamp,'source':capture.get('source','Jira MCP'),
            'complete':True,'issues':issues,
            'export_note':'Copia pública de contenido autorizado: omito correos, identificadores de cuenta y comentarios restringidos o internos. Conservo el original en Jira. No incluyo adjuntos binarios ni reacciones.'}
    paths=[]
    def write(name, text):
        p=folder/name
        with p.open('x',encoding='utf-8',newline='\n') as f:
            f.write(text)
        paths.append(p)
    write('captura.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    index=['# Captura de mis tareas de Jira', '',f'Consulta UTC: {stamp}.', '',record['export_note'],'',
           'Las descripciones y los comentarios siguientes son citas históricas; su redacción y fechas corresponden al original.','']
    for row in issues:
        index.append(f"- [{row['key']} — {row['summary']}]({row['key']}.md): {row['status']}")
        md=[f"# {row['key']} — {row['summary']}",'',f"[Abrir en Jira]({row['url']})",'',
            f"Estado observado: {row['status']}. Asignación: {row['assignee']}. Creación: {row['creator']}.",'',
            '## Descripción original consultada','',row['description'],'','## Comentarios conservados','']
        for c in row['comments']:
            md.extend([f"### {c['created']} — comentario {c['id']}",'',f"Autoría original: {c['author']}. [Abrir original]({c['url']}). Última edición informada: {c['updated']}.",'',c['body'],''])
        md.extend(['## Historial de cambios de campos',''])
        for e in row['changelog']:
            md.extend([f"### {e['created']} — cambio {e['id']}",'',f"Autoría original: {e['author']}.",''])
            for it in e['items']:
                md.extend([f"Campo: {it['field']}.",'',f"Antes: {it['fromString'] or '(sin valor informado)' }",'',f"Después: {it['toString'] or '(sin valor informado)' }",''])
        write(row['key']+'.md','\n'.join(md)+'\n')
    write('README.md','\n'.join(index)+'\n')
    manifest={'captured_utc':stamp,'content_sha256':fingerprint,'issues':len(issues),
              'comments':sum(len(i['comments']) for i in issues),
              'excluded_comments':sum(i['excluded_comments'] for i in issues),
              'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return folder

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada',type=Path,required=True)
    parser.add_argument('--salida',type=Path,default=Path(__file__).resolve().parents[1]/'historial-jira')
    args=parser.parse_args()
    capture=json.loads(args.entrada.read_text(encoding='utf-8-sig'))
    try:
        folder=save(capture,args.salida)
    except (ValueError,FileExistsError) as exc:
        parser.exit(1,f'No guardé la captura: {exc}\n')
    print(str(folder) if folder else 'Sin cambios: conservo la captura anterior.')

if __name__=='__main__':
    main()
