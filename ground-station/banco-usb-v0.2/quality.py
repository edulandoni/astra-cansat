"""ASTRA-22/34: avisos explicables del banco; no diagnostico sensores averiados."""
import math


def quality_flags(snapshot, telemetry_max_age=3., gps_max_age=3.):
    for limit in (telemetry_max_age, gps_max_age):
        if not math.isfinite(limit) or limit <= 0:
            raise ValueError('Umbrales de antigüedad finitos y positivos requeridos')
    data = snapshot.get('latest')
    expecting = not snapshot.get('done') and snapshot.get('status') != 'Reproducción terminada'
    no_fix = bool(data and data['GPS_SATS'] == '0')
    age, gps_age = snapshot.get('data_age'), snapshot.get('gps_age')
    storage = snapshot.get('storage', [])
    return {
        'telemetry_stale': bool(expecting and data and age is not None and age > telemetry_max_age),
        'gps_no_fix': no_fix,
        'gps_stale': bool(expecting and data and not no_fix and age is not None and age <= telemetry_max_age
                          and gps_age is not None and gps_age > gps_max_age),
        'mission_clock_frozen': bool(snapshot.get('clock_warning')),
        'ambiguous_context': bool(snapshot.get('ambiguous')),
        'storage_error': any(bool(d.get('error')) for d in storage),
        'known_storage_loss': any(d.get('dropped', 0) > 0 for d in storage),
        'loss_detail_incomplete': any(d.get('loss_ledger_truncated', False) for d in storage),
    }
