import fiftyone as fo

def display_dataset(dataset, open_tab):
    session = fo.launch_app(dataset, auto=False)
    if open_tab:
        session.open_tab()