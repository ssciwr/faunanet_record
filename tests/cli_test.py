from click.testing import CliRunner
from iSparrowRecord import cli
from pathlib import Path
import pytest


def test_cli_install(folders, empty_data_folder):
    _, _, custom_cfg = folders

    runner = CliRunner()

    result_install = runner.invoke(cli.install, str(Path(custom_cfg)))

    assert result_install.exit_code == 0

    output = result_install.output.split("\n")

    assert output == [
        "Creating iSparrow folders and downloading data",
        f"...using install config {custom_cfg}",
        "...making directories",
        "Installation finished",
        "",
    ]

    result_install_failed = runner.invoke(cli.install, "nonexistant")

    assert result_install_failed.exit_code == 1

    output = result_install_failed.output.split("\n")
    assert output == [
        "Creating iSparrow folders and downloading data",
        "...using install config nonexistant",
        "",
    ]

    assert type(result_install_failed.exception) is FileNotFoundError
    assert result_install_failed.exception.args == (
        "The folder nonexistant/install.yml does not exist",
    )


def test_cli_run_default(folders, empty_data_folder):
    _, data, _ = folders

    runner = CliRunner()

    result = runner.invoke(cli.run)

    # make sure things ran smoothly
    assert result.exit_code == 0

    data_dirs = list(Path(data).iterdir())
    most_recent_folder = max(
        data_dirs, key=lambda folder: folder.stat().st_mtime, default=None
    )

    yml_count = 0
    wav_count = 0
    for filename in Path(most_recent_folder).iterdir():
        if filename.suffix == ".yml":
            yml_count += 1

        if filename.suffix == ".wav":
            wav_count += 1

    # check output
    assert yml_count == 1
    assert wav_count == 3


def test_cli_run_debug(empty_data_folder):
    runner = CliRunner()

    with pytest.warns(UserWarning) as warning_info:
        result = runner.invoke(cli.run, "--debug")

    assert result.exit_code == 0

    res = result.output.split("\n")
    print(res)
    assert res == [
        "start data collection",
        "...preparing config",
        "...creating runner",
        "start collecting data for  9  seconds with  3 seconds per file",
        "",
    ]

    assert (
        str(warning_info[0].message)
        == "Debug output currently not yet implemented. Will run, but without any debug output."
    )


def test_cli_run_custom(folders, empty_data_folder):
    _, data, cfgdir = folders

    runner = CliRunner()

    path = str(Path(cfgdir) / "custom_example.yml")

    result = runner.invoke(cli.run, f"--cfg={path}")

    assert result.exit_code == 0

    res = result.output.split("\n")

    assert res == [
        "start data collection",
        "...preparing config",
        "... ...using custom run config:  " + path,
        "...creating runner",
        "start collecting data for  8  seconds with  4 seconds per file",
        "",
    ]

    data_dirs = list(Path(data).iterdir())
    most_recent_folder = max(
        data_dirs, key=lambda folder: folder.stat().st_mtime, default=None
    )
    yml_count = 0
    wav_count = 0
    for filename in Path(most_recent_folder).iterdir():
        if filename.suffix == ".yml":
            yml_count += 1

        if filename.suffix == ".wav":
            wav_count += 1

    # check output
    assert yml_count == 1
    assert wav_count == 2


def test_cli_run_custom_replace(folders, empty_data_folder):
    _, data, cfgdir = folders

    runner = CliRunner()

    path = str(Path(cfgdir) / "custom_example.yml")

    dictstr = '\'{"Recording":{"length_s":2}}\''

    result = runner.invoke(cli.run, f"--cfg={path} --replace={dictstr}")

    assert result.exit_code == 0

    data_dirs = list(Path(data).iterdir())

    most_recent_folder = max(
        data_dirs, key=lambda folder: folder.stat().st_mtime, default=None
    )

    yml_count = 0

    wav_count = 0

    for filename in Path(most_recent_folder).iterdir():
        if filename.suffix == ".yml":
            yml_count += 1

        if filename.suffix == ".wav":
            wav_count += 1

    # check output
    assert yml_count == 1
    assert wav_count == 4
