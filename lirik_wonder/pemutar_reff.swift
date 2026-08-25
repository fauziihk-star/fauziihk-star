import AVFoundation
import Foundation

// Argumen: file audio, detik mulai, dan durasi yang akan diputar.
guard CommandLine.arguments.count == 4,
      let mulai = TimeInterval(CommandLine.arguments[2]),
      let durasi = TimeInterval(CommandLine.arguments[3]) else {
    fputs("Pemakaian: pemutar_reff <audio> <mulai> <durasi>\n", stderr)
    exit(1)
}

do {
    let url = URL(fileURLWithPath: CommandLine.arguments[1])
    let pemutar = try AVAudioPlayer(contentsOf: url)
    pemutar.currentTime = mulai
    pemutar.prepareToPlay()
    pemutar.play()

    RunLoop.current.run(until: Date().addingTimeInterval(durasi))
    pemutar.stop()
} catch {
    fputs("Gagal memutar audio: \(error.localizedDescription)\n", stderr)
    exit(1)
}
