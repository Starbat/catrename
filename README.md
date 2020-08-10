# catrename

You want to rename a bunch of files. A common task. It gets complicated when you need to follow certain rules for different files. Do not panic. catrename to the rescue!

For help run:
```bash
python3 -m catrename -h
```

## Example

### Define categories
You took these pictures at the birthday party of your friend on 17.2.2015. They look something like `IMG_20150217_221151.jpg`. Pretty ugly and not very human-readable. But we can do something about that. First we need to define a file category. Therefore we write a small yaml entry.

The category needs a name. Just for clarity. We call it `BobsBirthday`. To identify files matching in this category we define a regular expression that matches every jpg file from that day: `'.\*20150217.\*'` (Remember to put all regular expressions in quotation marks.)

In the category 'parts' we can now define all name components that should be used for the new name. We give each part of the name an identifier (`year`, `time`, `extension`) and define a regular expression for recognition. In the regular expressions, the round brackets include the section to be used. For each part you can optionally specify a function that is applied to it before it is used in the new file name. We use here `time_of_day` to convert the time into a word.

Finally we formulate a template how the new file name should be composed. The defined parts are addressed with dollar signs and curly brackets.

```yaml
BobsBirthday:
  identifier: '.*20150217.*\.jpg'
  parts:
    year:
      regex: 'IMG_(\d{4}).*'
    time:
      regex: '.*(\d{6})\.jpg'
      transform: 'time_of_day'
    extension:
      regex: '.*\.(\w+)$'
  template: '${year}_${time}_Bobs_birthday_party.${extension}'
```

To create regular expressions, [rubular](https://rubular.com/) is very useful.

### Run catrename
Call this command from the project directory.
```bash
python3 -m catrename path/to/IMG_20150217_221151.jpg
```

After running catrename our file will be renamed to `2015_evening_Bobs_birthday_party.jpg`.

## Categories

Every category entry looks something like this. It consists of a category name, an identifier, one or more parts to find in the file name and a template for the new name. Optionally a transformation can be performed on each part before putting it in the template. And then, if desired, a post-processing can be applied to the new name.

```yaml
category name:
  identifier: 'regular expression'
  parts:
    partA:
      regex: 'regular expression'
    partB:
      regex: 'regular expression'
      transform: 'a python function identifier'
  template: '${partA}_${partB}_something_other'
  postproc: 'a python function identifier'
```

Write your categories in categories.yaml to use them automatically when you call the program. It is also possible to select one of several yaml files. The file to be used can be specified with the -c flag.

Any number of categories can be written to a yaml file. Note, however, that problems can occur if identifiers overlap.

## Functions for post-processing and transformation

You can define functions in `transformations.py` and use them in your `categories.yaml`. The functions should only take a single string as argument. If your function takes multiple arguments, you can use it in combination with a lambda function.

```yaml
Report:
  identifier: '.*report.*'
  parts:
    year:
      regex: '^(\d{4})\D.*'
    month:
      regex: '^\d{4}([a-zA-Z]+)_.*'
      transform: 'lambda m: encode_month(m, "ENG")'
    account:
      regex: '.*_(\d{8}\d{,2})_.*'
    extension:
      regex: '.*\.(\w+)$'
  template: '${year}-${month}report_${account}.${extension}'
```

## Tests
Install the [pytest](https://docs.pytest.org) package.

```bash
pip3 install pytest
```

Run it from the project directory.

```bash
python3 -m pytest
```

## License

Copyright (C) 2020 Starbat

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
