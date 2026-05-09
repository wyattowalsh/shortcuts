# Clean Clipboard

Normalize clipboard text by trimming whitespace and removing common tracking parameters.

## Permissions

- Reads clipboard text.
- Writes the normalized text back to the clipboard.
- Does not use network, shell execution, URL schemes, or AI model actions.

## Security Notes

Clipboard access is interactive and user-visible, but clipboard data may be sensitive. This example keeps data on device and intentionally avoids network access.

## Runtime Status

Runtime execution is not enabled in this foundation slice. Static validation and linting are enabled.
