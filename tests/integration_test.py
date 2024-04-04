from iSparrowRecord import Runner
from iSparrowRecord import utils
from pathlib import Path

import librosa


def test_integration(install, folders):
    _, _, cfgdir = folders

    config = utils.read_yaml(Path(cfgdir) / "custom_example.yml")

    runner = Runner(config)

    runner.run()
    assert len(list(Path(runner.output_path).expanduser().iterdir())) == 3

    yaml_count = 0
    wav_count = 0
    unknown_count = 0

    for filename in Path(runner.output_path).iterdir():
        if filename.suffix == ".yml":
            yaml_count += 1

        elif filename.suffix == ".wav":
            wav_count += 1

            data, rate = librosa.load(
                Path(runner.output_path) / filename,
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
