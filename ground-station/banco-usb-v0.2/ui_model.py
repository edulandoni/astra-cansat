"""ASTRA-22: textos de operación; mantengo los nombres originales en archivos."""
from engine import display,telemetry_view

STATES={'LAUNCH_PAD':'En la base','ASCENT':'Subiendo','APOGEE':'Altura máxima','DESCENT':'Primer descenso',
        'PROBE_RELEASE':'Transición de descenso','PAYLOAD_RELEASE':'Segundo descenso','LANDED':'En tierra'}
SCENARIO_NAMES={'NOMINAL':'Vuelo normal','PACKET_LOSS':'Mensajes que no llegan','CORRUPTED_PACKET':'Mensajes dañados',
                'GPS_LOSS':'GPS sin posición','RESET':'Reinicio lógico simulado'}
SCENARIO_HELP={'NOMINAL':'Ensaya subida y bajada con valores inventados; la placa permanece en la mesa.',
 'PACKET_LOSS':'El emisor omite algunos mensajes a propósito. Los huecos se detectan al recibir un contador posterior.',
 'CORRUPTED_PACKET':'El emisor daña algunos mensajes. Recibirlos no significa que sean válidos o se guarden como mediciones.',
 'GPS_LOSS':'Durante un tramo no hay posición GPS válida. La última posición se conserva con su antigüedad.',
 'RESET':'Simula un cambio de identidad y contador. No corta la alimentación ni equivale a desenchufar la placa.'}
FIELDS_INFO={
 'STATE':('Etapa del vuelo','','Indica en qué momento está el ensayo: en la base, subiendo, en la altura máxima, descendiendo o en tierra. La etapa la informa la placa; no se deduce sólo por la forma del gráfico.'),
 'ALTITUDE':('Altura sobre el inicio','m','Distancia vertical respecto del lugar donde empieza el ensayo. Si comienza en cero, 100 m significa 100 metros por encima de ese punto. Al subir aumenta; al bajar disminuye. Puede dar un valor ligeramente negativo cerca del cero. No indica distancia horizontal ni altura sobre el nivel del mar.'),
 'PRESSURE':('Presión del aire','kPa','Indica la presión atmosférica. Normalmente disminuye al aumentar la altura y vuelve a subir durante el descenso. kPa significa kilopascales. En este ensayo la presión se genera junto con la altura simulada.'),
 'TEMPERATURE':('Temperatura','°C','Indica la temperatura en grados Celsius. Permite seguir su variación durante el ensayo. El valor que llega en esta simulación es inventado; no mide la temperatura de la computadora ni del procesador.'),
 'MISSION_TIME':('Hora del emisor','UTC','Hora que informa la placa para la muestra recibida. UTC es una referencia horaria común, distinta de la hora local de Argentina. No es el tiempo transcurrido desde que empezó el vuelo. Sincronizar hora UTC envía la referencia de la PC cuando el ensayo está en preparación.'),
 'PACKET_COUNT':('Contador del emisor','','Número con el que la placa identifica cada muestra de una ejecución. Por ejemplo, pasar de 10 a 13 deja un hueco de dos muestras: 11 y 12. Si empieza otra ejecución o la placa vuelve a arrancar, ese contador puede volver al inicio.'),
 'TEAM_ID':('Equipo de prueba','','Identifica al equipo al que corresponden los mensajes. En esta simulación se usa 1000 como identificador de prueba. No representa una identificación oficial asignada por el concurso.'),
 'MODE':('Tipo de datos','','Indica si el emisor identifica los valores como simulación o vuelo. En el ensayo de prueba se generan valores ficticios. Conectar la placa por USB no convierte esos valores en mediciones de sensores.'),
 'VOLTAGE':('Tensión de batería','V','Indica la tensión eléctrica que informa el emisor para la batería. V significa voltios. En esta simulación el valor es inventado: no mide la tensión del USB. Una tensión aislada no permite saber cuántos minutos de autonomía quedan.'),
 'CURRENT':('Consumo eléctrico','A','Indica la corriente eléctrica que informa el emisor. A significa amperios. Ayuda a observar cambios de consumo durante una maniobra; no es un porcentaje de batería ni energía acumulada. En este ensayo el valor es simulado.'),
 'GPS_TIME':('Hora de posición','UTC','Hora correspondiente a la posición GPS informada. Puede dejar de actualizarse aunque sigan llegando otros mensajes. La aplicación informa la edad de la última posición válida para que no se confunda una posición retenida con una reciente.'),
 'GPS_ALTITUDE':('Altura GPS','m s. n. m.','Altura de la posición GPS respecto del nivel del mar. La abreviatura significa metros sobre el nivel del mar. Tiene una referencia distinta de Altura sobre el inicio: dos números diferentes no implican por sí solos un error.'),
 'GPS_LATITUDE':('Latitud','°','Coordenada que ubica la posición al norte o al sur del ecuador. Los valores negativos corresponden al sur. Se lee junto con la longitud. Sin solución GPS, una posición retenida se identifica como última válida; no es una posición nueva.'),
 'GPS_LONGITUDE':('Longitud','°','Coordenada que ubica la posición al este o al oeste del meridiano de Greenwich. Los valores negativos corresponden al oeste. Se lee junto con la latitud. Las coordenadas del ensayo son inventadas y no representan la ubicación de tu PC.'),
 'GPS_SATS':('Satélites declarados','','Cantidad de satélites que informa el GPS simulado. En este ensayo, cero indica que no hay una solución de posición válida. Un número mayor no garantiza por sí solo una ubicación más precisa; también importa que el dato se actualice.'),
 'GYRO_R':('Giro eje R','rad/s','Indica qué tan rápido gira el modelo alrededor del eje R. rad/s significa radianes por segundo: aproximadamente 6,28 rad/s equivale a una vuelta por segundo. El signo distingue el sentido del giro. No es el ángulo al que está inclinado.'),
 'GYRO_P':('Giro eje P','rad/s','Indica qué tan rápido gira el modelo alrededor del eje P. El signo distingue el sentido del giro. Se interpreta junto con los ejes R e Y; no es una velocidad de desplazamiento ni un ángulo.'),
 'GYRO_Y':('Giro eje Y','rad/s','Indica qué tan rápido gira el modelo alrededor del eje Y. Un valor cercano a cero indica poco giro alrededor de ese eje. No permite calcular energía generada sin otras mediciones.'),
 'ACCEL_R':('Aceleración eje R','m/s²','Indica la aceleración del modelo en el eje R. Se expresa en metros por segundo al cuadrado. Describe cambios de movimiento, no la velocidad a la que está viajando.'),
 'ACCEL_P':('Aceleración eje P','m/s²','Indica la aceleración del modelo en el eje P. Se lee junto con los otros dos ejes. Un valor constante por sí solo no demuestra que un sensor esté averiado.'),
 'ACCEL_Y':('Aceleración eje Y','m/s²','Indica la aceleración del modelo en el eje Y. En esta simulación incluye una componente cercana a 9,81 m/s² asociada a la gravedad. Por eso puede ser distinta de cero aunque el modelo esté en la base. No es velocidad de descenso.'),
 'CMD_ECHO':('Eco en telemetría','','Texto con el que el emisor refleja una orden en la telemetría. NONE significa que no informa un eco. Para saber si una orden enviada fue aceptada, rechazada o ejecutada, consultá el resultado que aparece debajo de los controles.')}
GROUPS=[('Vuelo','Etapa del ensayo y condiciones de altura, presión y temperatura.',
         ['STATE','ALTITUDE','PRESSURE','TEMPERATURE','MISSION_TIME','PACKET_COUNT','MODE','TEAM_ID']),
 ('Energía','Valores ficticios; todavía no medimos batería o autonomía.', ['VOLTAGE','CURRENT']),
 ('Ubicación GPS','Coordenadas inventadas. Sin solución, conservo la última válida.',
         ['GPS_SATS','GPS_TIME','GPS_ALTITUDE','GPS_LATITUDE','GPS_LONGITUDE']),
 ('Movimiento','Giro y aceleración en tres ejes: R, P e Y.',
         ['GYRO_R','GYRO_P','GYRO_Y','ACCEL_R','ACCEL_P','ACCEL_Y','CMD_ECHO'])]
REASONS={'NOT_LAUNCH_PAD':'Sólo se permite al preparar el ensayo en la base.',
 'BAD_ARGUMENT':'Los parámetros de la orden no son válidos.','BAD_TIME':'La hora enviada está fuera del rango permitido.',
 'ID_CONFLICT':'El identificador ya se usó con otro contenido.','ID_EXPIRED':'La orden es demasiado antigua para verificarla.',
 'UNKNOWN_OPERATION':'El emisor no reconoce esta orden.'}
OPS={'RUN':'Iniciar ensayo','STOP':'Detener ensayo','CAL_ZERO':'Poner altura en cero',
      'SET_TIME':'Sincronizar hora UTC','POWER_STATUS':'Consultar batería y solar'}

def age(value):return 'sin dato previo' if value is None else f'{value:.1f} s'

def interruption_text(c):
    number=c['number'];duration=c.get('duration') or 0
    if c.get('reconnected_at') is None:return f'Corte {number}: {duration:.1f} s sin conexión. Faltantes aún no determinables.'
    result=c.get('result')
    if result=='same_run':return f"Corte {number}: duró {duration:.1f} s. Misma ejecución; hueco al volver: {c['gap_at_resume']} muestras."
    if result=='restarted':return f'Corte {number}: duró {duration:.1f} s. La placa volvió a arrancar; no puedo determinar cuántos mensajes faltaron.'
    if result=='new_run':return f'Corte {number}: duró {duration:.1f} s. Otra ejecución; no comparo sus contadores.'
    if result=='unknown':return f'Corte {number}: duró {duration:.1f} s. Identidad insuficiente para determinar faltantes.'
    return f'Corte {number}: USB volvió tras {duration:.1f} s; espero identidad y una muestra posterior para comparar.'

def presentation(s,stale_seconds=3):
    live=s.get('latest');historical=False
    data,retained=telemetry_view(s)
    if not data and s.get('last_sample'):
        data=display(s['last_sample']);historical=True
        if data.get('GPS_SATS')=='0':
            for k in ['GPS_TIME','GPS_ALTITUDE','GPS_LATITUDE','GPS_LONGITUDE']:data[k]=None
    replay=s.get('source')=='REPLAY';connected=s.get('transport_connected',False)
    if replay:
        title='Reproducción terminada' if s.get('status')=='Reproducción terminada' else 'Reproduciendo una grabación'
        explanation='No recibo datos en vivo y no envío órdenes a la placa.'
    elif not connected:
        title='Placa desconectada' if s.get('ever_connected') else 'Buscando la placa'
        explanation='Intento reconectar automáticamente. Los valores conservados son históricos; no hay mediciones actuales.'
        if s.get('manual_closed'):
            title='Conexión USB cerrada desde la aplicación'
            explanation='Usá Conectar USB para volver a recibir. Cerrar el puerto no garantiza detener la emisión de la placa.'
    elif s.get('waiting_identity') or s.get('ambiguous'):
        title='USB conectado; verificando la identidad'
        explanation='Espero confirmar qué arranque y ejecución envían los datos; no mezclo contadores anteriores.'
    elif s.get('done'):
        title='Ensayo terminado';explanation='No se esperan más muestras. Iniciar ensayo crea otra ejecución y conserva ésta.'
    elif s.get('paused'):
        title='Ensayo detenido';explanation='La orden de detener fue ejecutada en simulación. El USB sigue conectado.'
    elif not live:
        title='Placa conectada; sin muestra actual';explanation='Esperando datos. Si está en reposo, elegí un escenario e iniciá el ensayo.'
    elif s.get('data_age',0)>stale_seconds:
        title='Conectado; datos sin actualizar';explanation='El puerto sigue abierto, pero dejó de llegar telemetría reciente. No atribuyo una causa sin evidencia.'
    else:
        title='Recibiendo datos';explanation='La placa está enviando valores sintéticos. El equipo permanece sobre la mesa.'
    old=historical or (s.get('data_age') is not None and s['data_age']>stale_seconds) or not connected or bool(s.get('ambiguous'))
    if replay:old=False
    note=('ÚLTIMA MUESTRA CONSERVADA — no es una medición actual. ' if old and data else '')
    note+=f"Última muestra recibida hace {age(s.get('last_sample_age'))}."
    if s.get('done') or s.get('paused'):note+=' El ensayo no está emitiendo nuevas muestras.'
    values={}
    for k in FIELDS_INFO:
        v=data.get(k)
        if v is None:label='Sin solución' if k.startswith('GPS_') and data else '—'
        elif k=='STATE':label=STATES.get(v,v)
        elif k=='MODE':label={'S':'Simulación','F':'Vuelo declarado'}.get(v,v)
        else:label=v
        if v is not None and FIELDS_INFO[k][1]:label+=' '+FIELDS_INFO[k][1]
        if k in retained and v is not None:label+=' · última válida'
        values[k]=label
    cuts=s.get('interruptions',[])
    gap_value=str(s.get('observed_gaps',0));gap_note='Sólo esta ejecución; un hueco no prueba su causa.'
    if cuts:
        last=cuts[-1]
        if last.get('reconnected_at') is None or last.get('result')=='awaiting_identity':
            gap_value='Por determinar'
            gap_note=f"Ya observados en esta ejecución: {s.get('observed_gaps',0)}. El corte aún no se puede evaluar."
        elif last.get('result') in {'restarted','new_run','unknown'}:
            gap_note='Huecos de esta ejecución. La cantidad que faltó durante el corte es desconocida.'
    return dict(title=title,explanation=explanation,note=note,old=old,values=values,
                gap_value=gap_value,gap_note=gap_note,
                interruption=interruption_text(cuts[-1]) if cuts else 'Sin cortes USB registrados en esta sesión.',
                gps_note=('Sin posición válida. ' if data.get('GPS_SATS')=='0' else 'La cantidad de satélites no acredita precisión. ')+
                         ('Edad de la última posición válida: '+age(s.get('gps_age')) if not historical else 'Muestra histórica del emisor.'))

def command_text(c,current_epoch=None):
    if not c:return 'Todavía no envié una orden de operación.'
    states={'queued':'En cola para enviar','sent':'Enviada; esperando respuesta','accepted':'Aceptada; falta confirmar ejecución',
            'executed':'Ejecutada en simulación','rejected':'Rechazada por el emisor',
            'timeout':'Sin respuesta a tiempo; no sé si se ejecutó','unknown':'Resultado desconocido tras la interrupción'}
    reason=c.get('result',{}).get('reason') or c.get('reason','')
    result=c.get('result',{})
    previous=bool(result) and current_epoch is not None and (result.get('boot'),result.get('run'))!=tuple(current_epoch)
    return ('Resultado de otra ejecución · ' if previous else '')+OPS.get(c['op'],c['op'])+': '+states.get(c['state'],c['state'])+(' · '+REASONS.get(reason,reason) if reason else '')+(' · respuesta tardía' if c.get('late') else '')

def controls(s):
    available=s.get('source')!='REPLAY' and s.get('profile')=='bench-usb-0.2' and s.get('transport_connected') and bool(s.get('peer')) and not s.get('ambiguous')
    pending=any(c['state'] in {'queued','sent','accepted'} for c in s.get('commands',[]) if c['op'] in {'RUN','STOP','CAL_ZERO','SET_TIME'})
    base=available and not pending
    preparing=not s.get('latest') or s.get('latest',{}).get('STATE')=='LAUNCH_PAD'
    stopped=bool(s.get('done') or s.get('paused'))
    return {'RUN':base,'STOP':base and not stopped,'CAL_ZERO':base and preparing,
            'SET_TIME':base and preparing,'POWER_STATUS':available}
