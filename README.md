# suite_time_calculation

A Python script to parse XML test suite files and extract execution times.

## Usage

```bash
python xml_parser.py
```

## Description

The script:
1. Scans the current directory for all `.xml` files
2. Extracts `name` and `time` attributes from each XML root element
3. Sorts results by execution time (descending)
4. Outputs formatted results to `result.json`

## Output Format

Results are written to `result.json` with times formatted as:
- `X m. Y s.` for times >= 60 seconds
- `X.X s.` for times < 60 seconds

## Requirements

- Python 3.x (uses standard library only)
