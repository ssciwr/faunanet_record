from iSparrowRecord import Runner
from iSparrowRecord import utils
from pathlib import Path
from platformdirs import user_config_dir
import yaml
import librosa


def test_integration(install, folders):
    _, _, cfgdir = folders
    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")

    install_filepath = Path(user_config_dir("iSparrowRecord")) / "install.yml"
    with open(install_filepath, "r") as cfgfile:
        sparrow_config = yaml.safe_load(cfgfile)

    runner = Runner(config, dump_config=True)

    runner.run()
    assert len(list(Path(runner.output).expanduser().iterdir())) == 3

    yaml_count = 0
    wav_count = 0
    unknown_count = 0

    for filename in Path(sparrow_config["Directories"]["data"]).expanduser().iterdir():
        if filename.suffix == ".yml":
            yaml_count += 1

        elif filename.suffix == ".wav":
            wav_count += 1

            data, rate = librosa.load(
                Path(sparrow_config["Directories"]["data"]).expanduser() / filename,
                sr=32000,
                res_type="kaiser_fast",
            )
            assert librosa.get_duration(y=data, sr=rate) == 4
            assert rate == 32000
            assert len(data) == int((32000 * 4))  # sample rate * recording time

        else:
            unknown_count += 1

    assert yaml_count == 1
    assert wav_count == 2
    assert unknown_count == 0
