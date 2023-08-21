import json
from collections import Counter
from pathlib import Path

from .configuration import Config


class Histogram:
    def __init__(self, counter: Counter, config: Config) -> None:
        self._counter = counter
        self._config = config

    @classmethod
    def load(cls, config: Config) -> "Histogram":
        hist_path = Path(config.hist_file).expanduser()
        hist_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(hist_path, "r") as f:
                counter = Counter(json.load(f))
        except FileNotFoundError:
            counter = Counter()

        return cls(counter=counter, config=config)

    @property
    def counts(self) -> Counter:
        return self._counter

    def save(self) -> None:
        hist_path = Path(self._config.hist_file).expanduser()
        hist_path.parent.mkdir(parents=True, exist_ok=True)
        with open(hist_path, "w") as f:
            f.write(json.dumps(self._counter))

    def update(self, counter: Counter) -> "Histogram":
        self._counter.update(counter)
        for word in set(self._counter.keys()) & set(self._config.ignores):
            del self._counter[word]

        for word in list(self._counter.keys()):
            if len(word) < self._config.min_length:
                del self._counter[word]

        return self
