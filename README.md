# Wait Wait Don't Tell Me Audio Segment Downloader

A Python script that downloads show segment audio files for each [Wait Wait Don't Tell Me!](https://waitwait.npr.org/) show that aired, pulled from a copy of the [Wait Wait Stats Database](https://github.com/questionlp/wwdtm_database).

## Requirements

- Python 3.12 or higher (Python versions that are still supported by prior to 3.12 have not been tested)
- Copy of the Wait Wait Stats Database loaded on to a MySQL Server running version 8 or higher

## Installing

All dependencies for running the script are listed in the [requirements.txt](./requirements.txt) file and can be installed via `pip` using the following command:

```bash
python3 -m pip install -r requirements.txt
```

For dependencies required for developing this script, use the [requirements-dev.txt](./requirements-dev.txt) file instead.

```bash
python3 -m pip install -r requirements-dev.txt
```

## Caveats

This script has only been tested when starting download from the start of 2006 and downloads segments using a predefined URL format:

```text
https://ondemand.npr.org/anon.npr-mp3/npr/waitwait/{YYYY}/{MM}/{YYYYMMDD}_waitwait_{segment}.mp3
```

Where `segment` is a number from 1 through 10 and left-padded with zero.

Starting with the October 9, 2021 show, NPR published each show as one monolithic file.

Starting with the January 7, 2023 show, NPR changed the URL format to include UUIDs as the segment number. The script does not workaround that.

NPR does not include credits as part of their audio segments and musical interstitials between segments are usually excluded.

## Code of Conduct

This projects follows the code of conduct as outlined in [Contributor Convenant 3.0](https://www.contributor-covenant.org/version/3/0/code_of_conduct/).

A copy of the code of conduct with information on how to report possible violations are available in the [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) file.

## License

This script is released under the terms of the [MIT License](./LICENSE).
