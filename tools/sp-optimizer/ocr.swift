// Apple Vision OCR helper for ocr_learn.py.
//
// Usage: swift ocr.swift <image> [<image> ...]
// Emits one JSON object: {"<path>": [{"text","x","y","w","h","conf"}, ...], ...}
// Coordinates are normalized [0,1] with origin at the TOP-left (y flipped from
// Vision's bottom-left convention). Language correction is off so game terms
// and prices come through verbatim.
import Foundation
import ImageIO
import Vision

var out: [String: [[String: Any]]] = [:]

for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
        FileHandle.standardError.write("cannot read image: \(path)\n".data(using: .utf8)!)
        exit(1)
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(cgImage: img, options: [:])
    do { try handler.perform([request]) } catch {
        FileHandle.standardError.write("OCR failed on \(path): \(error)\n".data(using: .utf8)!)
        exit(1)
    }
    var lines: [[String: Any]] = []
    for obs in request.results ?? [] {
        guard let cand = obs.topCandidates(1).first else { continue }
        let b = obs.boundingBox
        lines.append([
            "text": cand.string,
            "x": b.origin.x,
            "y": 1.0 - b.origin.y - b.size.height,  // top-left origin
            "w": b.size.width,
            "h": b.size.height,
            "conf": Double(cand.confidence),
        ])
    }
    out[path] = lines
}

let data = try JSONSerialization.data(withJSONObject: out, options: [.sortedKeys])
FileHandle.standardOutput.write(data)
FileHandle.standardOutput.write("\n".data(using: .utf8)!)
