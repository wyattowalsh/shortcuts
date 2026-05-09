import AppIntents

@available(iOS 18.0, macOS 15.0, *)
public struct CleanClipboardIntent: AppIntent {
    public static let title: LocalizedStringResource = "Clean Clipboard Text"
    public static let description = IntentDescription("Trim whitespace and normalize clipboard text.")

    @Parameter(title: "Text")
    public var text: String

    public init() {}

    public func perform() async throws -> some IntentResult & ReturnsValue<String> {
        let cleaned = text.trimmingCharacters(in: .whitespacesAndNewlines)
        return .result(value: cleaned)
    }
}
