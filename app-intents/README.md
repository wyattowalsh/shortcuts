# App Intents

This directory is reserved for Swift packages, demo apps, snippets, and fixtures for Siri/App Shortcuts and App Intents.

App Intents examples are first-class project content, not appendix material. They should document phrase behavior, entity modeling, platform availability, privacy implications, and testability constraints.

## Contents

- `Package.swift` defines a lightweight Swift package for snippet validation.
- `CleanClipboardIntent.swift` is a minimal parameterized `AppIntent` returning cleaned text.
- `NetworkNoteIntent.swift` demonstrates a parameterized intent plus `AppEnum`.
- `AppShortcuts.swift` demonstrates `AppShortcutsProvider` phrase design.

## Availability

Examples target iOS 18 and macOS 15. Treat them as copyable snippets for app projects, not a shipped app binary. Validate with Xcode on macOS before using in production apps.
