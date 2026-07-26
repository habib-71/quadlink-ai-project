"""Fault-tolerant sound playback for QuadLink."""

import math
import os
from array import array

import pygame

from config import SOUND_DIR


class AudioManager:
    """Loads optional sound assets and silently ignores unavailable audio."""

    SOUND_FILES = {
        "click": "button_click.wav",
        "drop": "piece_drop.wav",
        "win": "win.wav",
        "lose": "lose.wav",
        "draw": "draw.wav",
    }
    MUSIC_FILE = "background_music.ogg"

    def __init__(self):
        self.enabled = False
        self.sound_enabled = True
        self.music_enabled = True
        self.music_volume = 0.35
        self.sounds = {}
        self.music_available = False
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            return

        for name, filename in self.SOUND_FILES.items():
            path = os.path.join(SOUND_DIR, filename)
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except (pygame.error, FileNotFoundError):
                # The game ships with synthesized effects, so external audio is optional.
                self.sounds[name] = self._create_fallback(name)

        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(0.55)

        try:
            pygame.mixer.music.load(os.path.join(SOUND_DIR, self.MUSIC_FILE))
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_available = True
        except (pygame.error, FileNotFoundError):
            pass

    def _create_fallback(self, name):
        """Create a short, distinct WAV-quality tone without asset files."""
        try:
            sample_rate, sample_size, channels = pygame.mixer.get_init()
            if abs(sample_size) != 16:
                return None

            profiles = {
                "click": ((760,), 0.055),
                "drop": ((170, 118), 0.12),
                "win": ((523, 659, 784), 0.30),
                "lose": ((392, 311, 233), 0.34),
                "draw": ((440, 440), 0.20),
            }
            notes, duration = profiles[name]
            frame_count = int(sample_rate * duration)
            samples = array("h")

            for frame in range(frame_count):
                progress = frame / frame_count
                note_index = min(int(progress * len(notes)), len(notes) - 1)
                frequency = notes[note_index]
                # Fast attack and soft exponential release avoid audible clicks.
                attack = min(1.0, progress * 35)
                envelope = attack * (1.0 - progress) ** 1.8
                value = int(math.sin(2 * math.pi * frequency * frame / sample_rate) * 17000 * envelope)
                for _ in range(channels):
                    samples.append(value)

            return pygame.mixer.Sound(buffer=samples.tobytes())
        except (pygame.error, ValueError, KeyError):
            return None

    def play(self, name):
        sound = self.sounds.get(name)
        if self.enabled and self.sound_enabled and sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass

    def set_sound_enabled(self, enabled):
        self.sound_enabled = enabled

    def set_music_enabled(self, enabled):
        """Store the runtime music preference and mute optional music if loaded."""
        self.music_enabled = enabled
        if self.enabled and self.music_available:
            try:
                pygame.mixer.music.set_volume(self.music_volume if enabled else 0.0)
            except pygame.error:
                pass

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, float(volume)))
        self.set_music_enabled(self.music_enabled)
