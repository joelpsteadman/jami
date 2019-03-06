song = new MIDI(
    key = "Bb major"
    time = "4/4"
    tracks = (
        (
            (1, 44, 0, 1) # (channel, pitch, start, duration)
            (1, 48, 1, 1)
            (1, 50, 0, 1)
            (1, 43, 0, 1)
            (1, 44, 0, 4)
            (2, 44, 0, 2)
            (2, 39, 0, 2)
            (2, 44, 0, 4)
        )
    )
)

midi = new MIDI(
    "time_signature_event(4,4)",
    "key_signature_event(-2)",
    "tempo_set_event(500000 mspq)", #mspq = microseconds per quarter note
    ""
)