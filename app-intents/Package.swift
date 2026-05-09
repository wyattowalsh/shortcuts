// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "ShortcutsAppIntentsLab",
    platforms: [
        .iOS(.v18),
        .macOS(.v15),
    ],
    products: [
        .library(name: "ShortcutsAppIntentsLab", targets: ["ShortcutsAppIntentsLab"]),
    ],
    targets: [
        .target(name: "ShortcutsAppIntentsLab"),
    ]
)
