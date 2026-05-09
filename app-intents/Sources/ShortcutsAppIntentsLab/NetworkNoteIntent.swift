import AppIntents

@available(iOS 18.0, macOS 15.0, *)
public struct NetworkNoteIntent: AppIntent {
    public static let title: LocalizedStringResource = "Prepare Network Note"
    public static let description = IntentDescription("Create a note request for an approved domain.")

    @Parameter(title: "Domain")
    public var domain: NoteDomain

    public init() {}

    public func perform() async throws -> some IntentResult & ReturnsValue<String> {
        .result(value: "Fetch note from \(domain.rawValue)")
    }
}

@available(iOS 18.0, macOS 15.0, *)
public enum NoteDomain: String, AppEnum {
    case example = "example.com"

    public static let typeDisplayRepresentation = TypeDisplayRepresentation(name: "Note Domain")
    public static let caseDisplayRepresentations: [NoteDomain: DisplayRepresentation] = [
        .example: "example.com",
    ]
}
