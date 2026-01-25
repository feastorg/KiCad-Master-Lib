# kmlib-local

FEAST's custom KiCad library organized into categorized KMLib\_\* symbol and footprint libraries. Components are grouped by function to improve discoverability and avoid naming conflicts with other libraries.

## Structure

```sh
kmlib-local/
├── symbols/
├── footprints/
├── blocks/
└── 3dmodels/
```

The KMLib\_\* prefix is used for all categorized libraries to prevent conflicts when added to KiCad's library manager.

See [docs/adding_components.md](../docs/adding_components.md) for detailed workflow and categorization guidelines.
