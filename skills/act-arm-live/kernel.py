"""Kernel helpers for ARM Live access through the Atmospheric data Community Toolkit."""

ARMLIVE_QUERY_URL = 'https://adc.arm.gov/armlive/data/query'
ARM_BROWSER_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'


def armlive_credentials():
    """Return (username, token) for ARM Live from the session environment.

    Raises with a pointer to registration if the credentials are absent.
    """
    import os

    user = os.environ.get('ARMUSER')
    token = os.environ.get('ARMTOKEN')
    if not user or not token:
        raise RuntimeError(
            'ARM Live credentials not found. Expected ARMUSER and ARMTOKEN in the '
            'environment (Customize -> Credentials -> Add Credential). Register for a '
            'token at https://adc.arm.gov/armlive/'
        )
    return user, token


def armlive_list_files(datastream, startdate, enddate, username=None, token=None):
    """Filenames ARM Live holds for a datastream over a date range, without downloading.

    Returns [] both for "no data in this window" and "no such datastream", so use it
    to probe candidate names cheaply before committing to a download.
    """
    import json
    import urllib.request

    if username is None or token is None:
        username, token = armlive_credentials()
    from act.utils import date_parser

    start = date_parser(startdate, return_datetime=True).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end = date_parser(enddate, return_datetime=True)
    if end.hour == 0 and end.minute == 0 and end.second == 0:
        end = end.replace(hour=23, minute=59, second=59)
    end = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    url = (
        f'{ARMLIVE_QUERY_URL}?user={username}:{token}&ds={datastream}'
        f'&start={start}&end={end}&wt=json'
    )
    req = urllib.request.Request(url, None, {'user-agent': ARM_BROWSER_UA})
    body = urllib.request.urlopen(req).read().decode('utf-8')
    if body[1:14] == '!DOCTYPE html':
        raise ConnectionRefusedError('ARM Live rejected the credentials (check ARMUSER/ARMTOKEN).')
    payload = json.loads(body)
    if not payload or payload.get('status') != 'success':
        return []
    return list(payload.get('files', []))


def armlive_download(datastream, startdate, enddate, output=None, time=None,
                     username=None, token=None):
    """Download a datastream into `output` (default ./data/<datastream>); returns file paths."""
    import os

    import act

    if username is None or token is None:
        username, token = armlive_credentials()
    if output is None:
        output = os.path.join('data', datastream)
    return act.discovery.download_arm_data(
        username, token, datastream, startdate, enddate, time=time, output=output
    )


def armlive_open(datastream, startdate, enddate, output=None, keep_variables=None,
                 cleanup_qc=True, time=None, username=None, token=None, **read_kwargs):
    """Download a datastream and return it as one xarray Dataset (None if no files).

    `cleanup_qc=True` is the default because ARM's bit-packed QC attributes have to be
    converted to CF flag_masks/flag_meanings before any qcfilter method sees them.
    """
    import act

    files = armlive_download(
        datastream, startdate, enddate, output=output, time=time,
        username=username, token=token,
    )
    if not files:
        return None
    return act.io.arm.read_arm_netcdf(
        sorted(files), keep_variables=keep_variables, cleanup_qc=cleanup_qc, **read_kwargs
    )


def armlive_subset(filenames, variables=None, filetype='csv', output=None,
                   username=None, token=None):
    """Server-side concatenate + variable-subset via the ARM Live `mod` API.

    `filenames` must be BARE ARM filenames (no directory). Returns the local path of
    the single concatenated file, which is what the underlying ACT call omits.
    """
    import os

    import act

    if username is None or token is None:
        username, token = armlive_credentials()
    if output is None:
        output = os.path.join('data', 'armlive_mod')
    names = [os.path.basename(f) for f in filenames]
    fname = act.discovery.download_arm_data_mod(
        username, token, names, variables=variables, filetype=filetype, output=output
    )
    if fname is None:
        return None
    return os.path.join(output, fname)


def arm_datastream_parts(name_or_path):
    """Split an ARM datastream name or filename into site/class/facility/level/date/time."""
    import act

    p = act.utils.DatastreamParserARM(str(name_or_path))
    return {
        'site': p.site,
        'datastream_class': p.datastream_class,
        'facility': p.facility,
        'level': p.level,
        'datastream': p.datastream,
        'date': p.date,
        'time': p.time,
    }


def arm_facility_latlon(site_code, facility_code=None):
    """Lat/lon for ARM facilities, e.g. arm_facility_latlon('sgp', 'E13')."""
    import act

    return act.utils.arm_site_location_search(site_code=site_code, facility_code=facility_code)
