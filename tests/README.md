# Public package smoke tests

From the repository root, run:

```text
python scripts/check_public_package.py . --allow-public-case-index
```

The full workspace acceptance matrix remains private to the development workspace because it references the local corpus and its test fixtures.
