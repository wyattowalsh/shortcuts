import AppIntents

@available(iOS 18.0, macOS 15.0, *)
public struct ShortcutsLabAppShortcutsProvider: AppShortcutsProvider {
    public static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: CleanClipboardIntent(),
            phrases: [
                "Clean clipboard with \(.applicationName)",
                "Normalize text using \(.applicationName)",
            ],
            shortTitle: "Clean Clipboard",
            systemImageName: "doc.on.clipboard"
        )
    }
}
