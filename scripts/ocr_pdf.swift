import Foundation
import PDFKit
import Vision
import AppKit
let args=CommandLine.arguments
let url=URL(fileURLWithPath:args[1]);let out=URL(fileURLWithPath:args[2]);let start=args.count>3 ? Int(args[3])! : 1
let doc=PDFDocument(url:url)!;let end=args.count>4 ? min(Int(args[4])!,doc.pageCount) : doc.pageCount
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
for n in start...end {
 let dest=out.appendingPathComponent(String(format:"%04d.txt",n))
 if FileManager.default.fileExists(atPath:dest.path){continue}
 autoreleasepool {
  guard let page=doc.page(at:n-1) else{return}
  let box=page.bounds(for:.mediaBox);let scale=min(2.0,1800.0/max(box.width,box.height));let w=Int(box.width*scale),h=Int(box.height*scale)
  guard let ctx=CGContext(data:nil,width:w,height:h,bitsPerComponent:8,bytesPerRow:0,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue) else{return}
  ctx.setFillColor(NSColor.white.cgColor);ctx.fill(CGRect(x:0,y:0,width:w,height:h));ctx.scaleBy(x:scale,y:scale);page.draw(with:.mediaBox,to:ctx)
  guard let image=ctx.makeImage() else{return}
  let req=VNRecognizeTextRequest();req.recognitionLevel = .accurate;req.usesCPUOnly=true;req.recognitionLanguages=["en-US"];req.usesLanguageCorrection=true
  do {try VNImageRequestHandler(cgImage:image,options:[:]).perform([req]);let lines=(req.results ?? []).sorted{a,b in abs(a.boundingBox.midY-b.boundingBox.midY)>0.008 ? a.boundingBox.midY>b.boundingBox.midY : a.boundingBox.minX<b.boundingBox.minX}.compactMap{$0.topCandidates(1).first?.string};try lines.joined(separator:"\n").write(to:dest,atomically:true,encoding:.utf8)}catch{fputs("Page \(n): \(error)\n",stderr)}
 }
 if n%10==0{print("OCR \(n)/\(end)");fflush(stdout)}
}
