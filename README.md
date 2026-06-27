# UTAutomation

UTAutomation is an offline VectorCAST .tst generation and traceability enrichment tool for C/C++ source files.

It scans C/C++ source files, parses functions and control flow, plans skeleton and condition-focused test cases, enriches metadata from ReviewID Excel files and GUID sources, writes VectorCAST-compatible .tst files, and optionally validates the generated output.

## Command

python UTAutomation.py -f <SourceFile> -o <OutputPath> -c <Config.yaml> [--validate] [--reviewid <file>] [--eapx <file>] [--guid-map <file>]
python UTAutomation.py -F <SourceFolder> -o <OutputPath> -c <Config.yaml> [--validate] [--reviewid <file>] [--eapx <file>] [--guid-map <file>]

## Required arguments

-f, --file: Source file path
-F, --folder: Source folder path
-o, --output: Output folder
-c, --config: YAML configuration file

Use either -f or -F, not both.

## Optional arguments

--validate / -validate: Validate generated .tst files
--reviewid <file>: ReviewID Excel file path (.xlsm/.xlsx)
--guid-map <file>: JSON GUID mapping file
--eapx <file>: EA repository path (.eapx/.eap/.qea/.qeax)
--eapx-backend <backend>: auto/access/sqlite/com, default auto

## Install

pip install -r requirements.txt

## Minimal YAML config

See ut_config.yaml.

## Examples

python UTAutomation.py -f .\tests\fixtures\source\App_SLI.c -o .\vcast_output -c .\ut_config.yaml --validate
python UTAutomation.py -F .\tests\fixtures\source -o .\vcast_output -c .\ut_config.yaml --validate
python UTAutomation.py -F .\tests\fixtures\source -o .\vcast_output -c .\ut_config.yaml --eapx .\model\design.qea --eapx-backend sqlite --validate

## GUID lookup priority

1. JSON GUID map if configured and matched.
2. EA repository via --eapx if configured and matched.
3. Missing marker from YAML (usually TBD).

UTAutomation never fabricates GUIDs.

## Output

vcast_output/<unit>.tst
vcast_output/utautomation_report.json

## ARXML note

YAML is the official config format. ARXML is not supported as the main config file.
