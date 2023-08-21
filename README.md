# deepler

deepler is a learning support tool that records the number of words that appear through DeepL.
You can learn frequently used words efficiently.

```bash
# DeepL API Free Plan is here.
# https://www.deepl.com/pro#developer
$ export DEEPL_AUTH_KEY=<YOUR API KEY>

$ pip install deepler
$ deepler
usage: deepler [-h] {translate,hist,configure} ...
deepler: error: the following arguments are required: {translate,hist,configure}
```

## Overview

```bash
# default configuration
$ deepler configure --show
{
  "ignores": [],
  "hist_file": "~/.config/deepler/counts.json",
  "min_length": 4,
  "source_lang": "EN",
  "target_lang": "JA",
  "count_lang": "EN"
}

$ deepler translate --text "deepler is a learning support tool that records the number of words that appear through DeepL."
input text(EN)
deepler is a learning support tool that records the number of words that appear through DeepL.

output text(JA)
deeplerは、DeepLを通じて出現した単語の数を記録する学習支援ツールです。

$ deepler hist
('that', 2)
('deepler', 1)
('learning', 1)
('support', 1)
('tool', 1)
('records', 1)
('number', 1)
('words', 1)
('appear', 1)
('through', 1)
('deepl', 1)

$ deepler translate --text "deepler is a learning support tool that records the number of words that appear through DeepL."
input text(EN)
deepler is a learning support tool that records the number of words that appear through DeepL.

output text(JA)
deeplerは、DeepLを通じて出現した単語の数を記録する学習支援ツールです。

$ poetry run deepler hist --num-words 3                                                                                                                                                                                                       [main]
('that', 4)
('deepler', 2)
('learning', 2)

$ poetry run deepler hist --min-count 3                                                                                                                                                                                                       [main]
('that', 4)
```

**Currently, only space-separated languages can be counted.**
