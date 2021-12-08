import os

from ..bidsname import get_bidsname_config, init_layout, get_ephys_filename


def test_get_bidsname_config_smoke_test():
    bidsname_config = get_bidsname_config()
    assert list(bidsname_config.keys()) == [
        "ephys_file",
        "ephys_file_rel_path",
        "scans_tsv",
        "sessions_tsv",
    ]


def test_init_layout_smoke_test():
    init_layout("data")


def test_get_ephys_filename():

    entities = {
        "subject": "01",
        "session": None,
        "sample": "A",
        "run": 1,
        "task": "nox",
        "suffix": "ephys",
        "extension": "nwb",
    }
    layout = init_layout("data")
    filename = get_ephys_filename(layout, entities)
    rel_path = filename.split("/")[-4:]
    assert (
        os.path.join(*rel_path)
        == "data/sub-01/ephys/sub-01_sample-A_task-nox_run-1_ephys.nwb"
    )
