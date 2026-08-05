# Other notes

## `patients_from_xml.json` vs `patients.json` vs `patients_from_cda_xml.json`

The first and second JSON only differ in how `conditions` array is handled when there is no conditions in origin.
The first one always creates an array with 0..* cardinality, whereas `conditions` field on the second one doesn't have a homogeneous criteria, meaning it can exist as an empty array or not exist at all.

However, the third JSON, even though it has the same structure as the first JSON, it will always have 0..1 patients because in EU ArtDecor CDA implementation, the field `recordTarget` always has a maximum cardinality of 1.
