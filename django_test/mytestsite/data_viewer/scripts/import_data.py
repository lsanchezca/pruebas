from data_viewer.import_data import import_data


def run(*args):
    normalized = {str(arg).strip().lower() for arg in args}
    clear_existing = bool(normalized.intersection({'clear', '--clear', 'true', '1'}))

    count = import_data(clear_existing=clear_existing)
    print(f'Imported {count} rows into data_viewer_dataentry.')
