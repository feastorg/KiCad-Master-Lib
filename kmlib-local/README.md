# kmlib-local

FEAST's custom KiCad library organized into categorized KMLib_* symbol and footprint libraries. Components are grouped by function to improve discoverability and avoid naming conflicts with other libraries.

## Structure

```
kmlib-local/
├── symbols/          # 13 categorized .kicad_sym libraries + legacy kml-custom
├── footprints/       # 12 categorized .pretty folders + legacy kml-custom
└── 3dmodels/         # 10 categorized .3dshapes folders
```

The KMLib_* prefix is used for all categorized libraries to prevent conflicts when added to KiCad's library manager. A legacy `kml-custom` library is maintained for backward compatibility with existing projects.

See [docs/adding_components.md](../docs/adding_components.md) for detailed workflow and categorization guidelines.
