from pathlib import Path
import argparse
from datetime import datetime
from set_up_fake_sparrow import set_up
import time

from iSparrowRecord import Recorder
from iSparrowRecord import utils

parser = argparse.ArgumentParser(description="iSparrowRecord CLI")

parser.add_argument(
    "--cfg",
    default="default",
    help="Optional user defined yaml file providing arguments for data collection. (default: %(default)s)",
)

parser.add_argument(
    "--standalone",
    help="Whether SparrowRecorder runs alone or in conjunction with other Sparrow modules. (default: False)",
    action="store_true"
)

args = parser.parse_args()

def main():
    """
    main Collect data until a certain datetime has been reached, 
    or for a certain amount of seconds or indefinitely. 
    Uses a yaml user supplied yaml file to update the default arguments and stores it together with the data.
    """
    runs_standalone = args.standalone

    if runs_standalone:
        print("setting up sparrow")
        set_up()

    config = _process_configs()

    end_time = _process_runtime(config)

    output = str(Path(config["Output"]["output_folder"]).expanduser())

    # create recorder, then start
    recorder = Recorder(output_folder=str(Path(output).expanduser()), **config["Recording"])

    if end_time is None:
        # run forever
        recorder.start(lambda x: False)

    if isinstance(end_time, int):
        begin_time = time.time()
        # run until time passed
        recorder.start(lambda x: time.time() > begin_time + end_time)

    if isinstance(end_time, datetime):
        # run until date is reached
        recorder.start(lambda x: datetime.now() > end_time)


if __name__ == "__main__":
    main()
