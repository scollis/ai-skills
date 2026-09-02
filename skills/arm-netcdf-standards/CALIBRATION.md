# ARM standards checker: calibration against released ARM data

Standard: **DOE/SC-ARM-15-004 v1.3 (September 2020)** · profile: `adc`

Files checked: **143** (one per datastream, six local data trees), of which **140** carry ARM-conforming filenames. **95** of those have no required-standard violation.

| data level | files | free of errors |
|---|---|---|
| `a1` | 19 | 7 |
| `b1` | 95 | 73 |
| `c0` | 2 | 0 |
| `c1` | 24 | 15 |

This table is calibration, not judgement. A rule firing on most released ARM files is either a real legacy deviation the standard itself records (§3.1 retired `unitless`; §6.8.8 argues against `valid_min` as a QC limit), or a bug in the rule. Every row below was traced back to the source document before being kept; five rules were relaxed or re-pointed during this exercise because released files proved them wrong.

## Every rule that fired

| severity | rule | section | files | findings | example message |
|---|---|---|---|---|---|
| error | `ATT-004` | 6.6.1 | 20 | 246 | units = 'unitless'; unitless quantities are represented by the UDUNITS value '1' |
| error | `QC-004` | 6.8.2 | 11 | 179 | units = 'unitless'; a QC variable requires units = '1' |
| error | `QC-008` | 6.8.2/6.8.11 | 10 | 316 | flag_method is required and must be 'bit' (bit-packed) or 'integer' (single-state) |
| error | `TIM-014` | 6.1.3 | 8 | 8 | standard_name = 'time' is required on the CF time coordinate |
| error | `GLB-004` | 6.7 | 6 | 7 | global attribute 'comment' has an empty value; if unknown use 'unknown', -9999, or 'N/A' |
| error | `ATT-006` | 6.6.4 | 6 | 161 | standard_name = 'radar_correlation_coefficient_copolar_h_crosspolar_v' is not in the CF standard-name table; inventing a new value is not allowed |
| error | `SRC-010` | 6.9.4/6.9.5 | 5 | 5 | long_name = 'Source for field: Best Estimate Global Downwelling Shortwave Hemispheric Irradiance'; the required form is 'Source for variable: <data va |
| error | `ATT-020` | 6.6.6 | 4 | 4 | sensor_height = '0 m'; the format is '<value> <udunits unit> AGL' separated by single spaces |
| error | `GLB-001` | 6.7.1 | 4 | 18 | required global attribute 'Conventions' is missing |
| error | `TIM-006` | 6.1.2 | 4 | 4 | ancillary_variables must be set to 'time_offset' to link the pair |
| error | `TIM-010` | 6.1.2 | 4 | 4 | ancillary_variables must be set to 'base_time' to link the pair |
| error | `QC-001` | 6.8.2 | 4 | 40 | data variable does not list 'qc_time' in its ancillary_variables attribute, which is required to link the pair |
| error | `CRD-003` | 6.2 | 3 | 4 | a coordinate variable may not have missing_value or _FillValue |
| error | `LOC-003` | 6.3 | 3 | 9 | standard_name = None; 'latitude' is required |
| error | `FILE-001` | 4.0 | 2 | 2 | file cannot be opened as netCDF: [Errno 2] No such file or directory: '/Users/scollis/data/bnf_precip/arm_order_268178/bnfcsapr2cfrS3.a1/ppi/bnfcsapr2 |
| error | `QC-027` | 6.8.3 | 1 | 1 | data set bit(s) [4] that no bit_<#>_description declares; every set bit must have a description |
| error | `STA-008` | 6.5.1/6.5.2 | 1 | 1 | flag_values = '1 0 -1 -2 -3' is stored as a character attribute; it must be a numeric array of the same type as the variable (e.g. flag_values = 0, 1, |
| error | `STA-010` | 6.8.8 | 1 | 1 | state values are embedded in the data but no valid_min/valid_range is declared, so software cannot exclude them; the flag_values must lie outside the  |
| error | `LVL-001` | 5.1.3 | 1 | 1 | a b-level datastream requires QC checks applied to at least one measurement and stored in an accompanying QC variable (qc_time alone does not make a d |
| error | `QC-019` | 6.8.3 | 1 | 15 | flag_1_assessment = 'Acceptable'; the only options are 'Bad' and 'Indeterminate' |
| warning | `GLB-002` | 6.7.1 | 137 | 138 | absent: command_line_comment, title, institution, description, references, doi_url -- printed bold-underline (therefore required) in section 6.7.1, bu |
| warning | `ATT-010` | 6.8.8 | 105 | 3149 | valid_min is present on a data variable; valid_min/valid_max are absolute limits of usable data, not QC limits -- use fail_min/fail_max (or warn_min/w |
| warning | `FILE-007` | 5.1 | 50 | 50 | '.cdf' is allowed for historical data only; use '.nc' for new and reprocessed files |
| warning | `QC-006b` | 3.1/6.8.2 | 32 | 592 | long_name uses the legacy wording 'on field:'; version 1.3 of the standard uses the term 'variable' only, so the form is 'Quality check results on var |
| warning | `GLB-018` | 6.7.1 | 25 | 29 | sampling_interval = '1/(10 kHz)' should be a value and a UDUNITS descriptor separated by a single space (e.g. '400 us', '5 minute') |
| warning | `CRD-006` | 6.2.1/6.2.2 | 22 | 23 | a vertical coordinate must document its frame of reference with standard_name: 'height' for AGL, 'altitude' for MSL (long_name is not the official met |
| warning | `CRD-001` | 6.2 | 17 | 29 | dimension has no same-named coordinate variable; one with long_name and units is recommended unless the dimension is a string length or index |
| warning | `ATT-005` | 6.6.1/App. C | 12 | 65 | units = 'oktas': symbol(s) ['oktas'] not recognised as UDUNITS; verify against the UDUNITS-2 database and Appendix C |
| warning | `FMT-002` | 4.0 | 11 | 11 | netCDF-4 (extended model) is used; ARM's preferred final format is the netCDF-3 model, with netCDF-4 *classic* allowed for compression |
| warning | `GLB-016` | 6.7.1 | 6 | 6 | institution must match the value fixed by the standard exactly: 'United States Department of Energy - Atmospheric Radiation Measurement (ARM) program' |
| warning | `SRC-017` | 6.9.4 | 5 | 5 | one integer source value must describe the no-source/default case with flag_<#>_description = 'no_source_available' |
| warning | `STA-009` | 6.8.8 | 4 | 11 | flag_values are mixed into a floating-point data variable; mixing state or QC information with the observed values is not recommended |
| warning | `GLB-015` | 6.7.1 | 4 | 4 | doi = 'DOI:10.5439/1178582' is not of the form '10.xxxx/yyyy' |
| warning | `GLB-009b` | 6.7.1 | 4 | 4 | facility_id = 'C1: Lamont, Oklahoma' appends a description; the documented value is the identifier alone ('C1') -- the location belongs in location_de |
| info | `GLB-003` | 6.7.1 | 137 | 138 | absent, required only under their stated condition: input_source (ingest only; required if reading RAW data); serial_number (ingest only; required if  |
| info | `BND-001` | 6.1.4 | 82 | 83 | no time bounds variable; for all non-instantaneous data the bounds of each averaging period are required |
| info | `QC-028` | 6.8.2 | 32 | 592 | standard_name = 'quality_flag' is recommended for QC variables |
| info | `VAR-005` | 6.4 | 18 | 314 | upper-case letters should be used sparingly in variable names |
| info | `QC-016` | 6.8.2/6.8.11 | 17 | 144 | description differs from the wording given in the standard; the exact sentence is what automated tools look for |
| info | `ATT-011` | 6.6 | 10 | 549 | attribute 'B1': variable attribute names are lower case with words separated by underscores |
| info | `FMT-001` | 4.0 | 7 | 7 | netCDF-4 classic model: allowed for high-volume data to use compression, and expected to reduce volume by at least 50% |
| info | `STA-003` | 6.5.1 | 6 | 8 | individual flag meanings are words joined with underscores |
| info | `CRD-007` | 6.2.1 | 6 | 6 | standard_name = 'projection_range_coordinate'; AGL is declared with 'height' and MSL with 'altitude' |
| info | `ATT-012` | 6.6 | 6 | 6 | 2 comment_<#> attributes; a single lengthy comment, or descriptively named comments, are preferred |
| info | `FILE-012` | 5.1 | 5 | 5 | instrument/qualifier 'wbpluvio2' ends with a digit, which can be confused with a temporal-resolution descriptor; allowed when the digit enumerates ins |
| info | `VAR-004` | 6.4 | 5 | 13 | single-character names are not recommended |
| info | `ATT-002` | 6.6.1 | 5 | 15 | the first letter of long_name is recommended to be capitalised |
| info | `ATT-001` | 6.6.1 | 4 | 4 | long_name is recommended on a bounds variable |
| info | `QC-024` | 6.8.10 | 3 | 6 | QC is dimensionally summarised (('time',) vs ('time', 'range_bins')); the summarising method must be described in an attribute or a technical document |
| info | `SRC-003` | 6.9.1 | 1 | 1 | source token 'bnfaosccn200M1.20260618.000000.eta_table_b' matches no variable in this file, so it is read as an algorithm name; algorithm identifiers  |
