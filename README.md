# gcmodeldev-cmor-tables
Prototype set of MIP tables that are being used for experimentation with CMORising HadGEM3 GC model data

These tables are adapted from those put together for CMIP6, but are primarily intended for experimentation with using CDDS for Met Office Model Development runs

Tables are defined in /definitions/variable_tables/*.json. Legacy format tables are regenerated from these and kept in /legacy_tables/*.json for backward compatibility. 

The data properties are defined in utils/entities.py and in the derivative schema/*.schema.json files. The schema.json files can be used to instruct IDE's to auto-validate and typehint the variable table files as you edit them. The entities.py file uses Pydantic class to specify property types and validate data when you load it - turning python's dataclass approach into a strongly typed definition. For more information see https://pydantic-docs.helpmanual.io/

Helper scripts are found in utils and include
- schema generator - produces json schema for the key json files
- table_converter - python script that includes methods for loading and saving legacy / new style json files

On push all definitions/variable_tables/*.json files will be validated by unit tests

On pull request the generated schema and legacy tables will be regenerated automatically (if not manually run using the utils scripts)

### old to new table format changes:
- File naming convention has changed with old being "GCModelDev_tablename.json" whilst new are "tablename.json"
- Optional values are optional rather than ""
- Lists are just that rather than space separated within a single string
- Dates are iso format
- Numeric values are no longer hidden in strings
- Key casing is consistent (all lower case) rather than mixed with some capitalised and some lower
- Some minor re-ordering to put optional properties after mandatory