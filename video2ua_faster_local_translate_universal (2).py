#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Video -> faster-whisper -> local multilingual translation -> TXT/SRT.

Якщо мова оригіналу (визначена або задана через --language) збігається
з --target, переклад пропускається: скрипт лише розпізнає мову і
одразу зберігає TXT/SRT з оригінальним текстом (наприклад, аудіо вже
українською -> просто витяг субтитрів без NLLB)."""

""" 
Якщо вискакує помилка: RuntimeError: Library libcublas.so.12 is not found or cannot be loaded

pip install -U nvidia-cublas-cu12 nvidia-cudnn-cu12;export LD_LIBRARY_PATH="$VIRTUAL_ENV/lib/python3.13/site-packages/nvidia/cublas/lib:$VIRTUAL_ENV/lib/python3.13/site-packages/nvidia/cudnn/lib:$LD_LIBRARY_PATH"
"""


import argparse
import os
import subprocess
import sys
from pathlib import Path

# Whisper code -> NLLB code.
NLLB_LANGS = {
    "en": "eng_Latn", "uk": "ukr_Cyrl", "ru": "rus_Cyrl",
    "pl": "pol_Latn", "de": "deu_Latn", "fr": "fra_Latn",
    "es": "spa_Latn", "it": "ita_Latn", "pt": "por_Latn",
    "cs": "ces_Latn", "sk": "slk_Latn", "ro": "ron_Latn",
    "hu": "hun_Latn", "nl": "nld_Latn", "sv": "swe_Latn",
    "no": "nob_Latn", "da": "dan_Latn", "fi": "fin_Latn",
    "tr": "tur_Latn", "bg": "bul_Cyrl", "sr": "srp_Cyrl",
    "hr": "hrv_Latn", "sl": "slv_Latn", "el": "ell_Grek",
    "he": "heb_Hebr", "ar": "arb_Arab", "fa": "pes_Arab",
    "hi": "hin_Deva", "ja": "jpn_Jpan", "ko": "kor_Hang",
    "zh": "zho_Hans", "vi": "vie_Latn", "id": "ind_Latn",
    "th": "tha_Thai",
}

LANG_NAMES = {
    "en": "English", "uk": "Ukrainian", "ru": "Russian",
    "pl": "Polish", "de": "German", "fr": "French",
    "es": "Spanish", "it": "Italian", "pt": "Portuguese",
    "cs": "Czech", "sk": "Slovak", "ro": "Romanian",
    "hu": "Hungarian", "nl": "Dutch", "sv": "Swedish",
    "no": "Norwegian", "da": "Danish", "fi": "Finnish",
    "tr": "Turkish", "bg": "Bulgarian", "sr": "Serbian",
    "hr": "Croatian", "sl": "Slovenian", "el": "Greek",
    "he": "Hebrew", "ar": "Arabic", "fa": "Persian",
    "hi": "Hindi", "ja": "Japanese", "ko": "Korean",
    "zh": "Chinese", "vi": "Vietnamese", "id": "Indonesian",
    "th": "Thai",
}

NLLB_MODEL = "facebook/nllb-200-distilled-600M"


def setup_cuda_library_path():
    """Expose CUDA libraries installed by pip to CTranslate2."""
    paths = []
    try:
        import nvidia.cublas
        paths.append(Path(nvidia.cublas.__path__[0]) / "lib")
    except Exception:
        pass
    try:
        import nvidia.cudnn
        paths.append(Path(nvidia.cudnn.__path__[0]) / "lib")
    except Exception:
        pass

    paths = [str(p) for p in paths if p.is_dir()]
    if paths:
        old = os.environ.get("LD_LIBRARY_PATH", "")
        os.environ["LD_LIBRARY_PATH"] = ":".join(paths + ([old] if old else []))


def extract_audio(video_path, wav_path):
    """Витягує аудіодоріжку з відео (будь-який формат, який підтримує ffmpeg)
    у WAV 16kHz mono — саме такий формат очікує faster-whisper."""
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_path), "-vn",
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(wav_path)
    ], check=True)


def load_whisper(model_name):
    """Завантажує модель faster-whisper. Спершу пробує CUDA (float16),
    якщо GPU недоступна — відкат на CPU (int8). Повертає (model, device)."""
    from faster_whisper import WhisperModel
    try:
        model = WhisperModel(model_name, device="cuda", compute_type="float16")
        print("[Whisper] Device: CUDA, compute: float16")
        return model, "cuda"
    except Exception as exc:
        print(f"[Whisper] CUDA недоступна: {exc}")
        print("[Whisper] Переходжу на CPU...")
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        print("[Whisper] Device: CPU, compute: int8")
        return model, "cpu"


def transcribe_audio(model, wav_path, language):
    """Розпізнає мову в аудіофайлі. language=None -> автовизначення мови.
    Повертає (segments, info), де info.language — визначена/задана мова."""
    # Important: faster-whisper returns a lazy generator, so CUDA errors
    # can appear only at list(segments).
    try:
        segments, info = model.transcribe(
            str(wav_path),
            language=language,
            vad_filter=True,
            beam_size=5,
        )
        return list(segments), info
    except Exception as exc:
        if language is not None:
            raise
        print(f"[Whisper] Помилка під час автоматичного розпізнавання: {exc}")
        print("[Whisper] Пробую CPU...")
        from faster_whisper import WhisperModel
        cpu_model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = cpu_model.transcribe(
            str(wav_path), language=None, vad_filter=True, beam_size=5
        )
        return list(segments), info


class NLLBTranslator:
    """Локальний перекладач тексту на базі NLLB-200
    (facebook/nllb-200-distilled-600M). Модель завантажується один раз
    у __init__, далі translate() можна викликати скільки завгодно разів."""

    def __init__(self, source_lang, target_lang, device):
        """source_lang/target_lang — коди мов Whisper ('en', 'uk', ...),
        які тут мапляться у коди NLLB через словник NLLB_LANGS."""
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        if source_lang not in NLLB_LANGS:
            raise ValueError(f"Немає NLLB-коду для мови: {source_lang}")
        if target_lang not in NLLB_LANGS:
            raise ValueError(f"Немає NLLB-коду для мови: {target_lang}")

        self.source = NLLB_LANGS[source_lang]
        self.target = NLLB_LANGS[target_lang]
        self.device = device if device == "cuda" and torch.cuda.is_available() else "cpu"

        print(f"[Translate] Модель: {NLLB_MODEL}")
        print(f"[Translate] {source_lang} -> {target_lang}")
        print(f"[Translate] Device: {self.device}")

        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            NLLB_MODEL, torch_dtype=dtype
        ).to(self.device)
        self.model.eval()

    def translate(self, texts, batch_size=8):
        """Перекладає список рядків батчами по batch_size, повертає
        список перекладених рядків у тому самому порядку."""
        import torch

        self.tokenizer.src_lang = self.source
        target_id = self.tokenizer.convert_tokens_to_ids(self.target)
        result = []

        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            encoded = self.tokenizer(
                batch, return_tensors="pt", padding=True,
                truncation=True, max_length=512
            ).to(self.device)

            with torch.inference_mode():
                generated = self.model.generate(
                    **encoded,
                    forced_bos_token_id=target_id,
                    max_length=512
                )

            result.extend(self.tokenizer.batch_decode(
                generated, skip_special_tokens=True
            ))
            print(
                f"[Translate] {min(start + batch_size, len(texts))}/{len(texts)}",
                end="\r", flush=True
            )

        print()
        return result


def srt_time(seconds):
    """Формат часової мітки для SRT: HH:MM:SS,mmm"""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def save_srt(path, segments, texts):
    """Записує .srt: для кожного сегмента бере його таймінг (start/end)
    і відповідний рядок з texts (перекладений або оригінальний)."""
    lines = []
    for i, (seg, text) in enumerate(zip(segments, texts), 1):
        lines += [
            str(i),
            f"{srt_time(seg.start)} --> {srt_time(seg.end)}",
            text.strip(), ""
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    """Точка входу: відео -> аудіо (ffmpeg) -> розпізнавання (faster-whisper)
    -> переклад (NLLB), якщо мова оригіналу відрізняється від --target
    -> TXT + SRT. Якщо мова оригіналу вже дорівнює --target, переклад
    пропускається і зберігається лише розпізнаний текст."""
    p = argparse.ArgumentParser(
        description="Відео -> аудіо -> розпізнавання -> (за потреби) переклад -> TXT/SRT"
    )
    p.add_argument("video", type=Path, help="Шлях до відеофайлу")
    p.add_argument("--model", choices=["tiny", "base", "small", "medium", "large-v3"],
                   default="small",
                   help="Розмір моделі faster-whisper: більша = точніше, але повільніше")
    p.add_argument("--language", default="auto",
                   help="Source language: auto, en, uk, ru, pl, de, ...")
    p.add_argument("--target", default="uk",
                   help="Target language: uk, en, pl, de, ...")
    p.add_argument("--batch-size", type=int, default=8,
                   help="Розмір батчу для перекладу NLLB (більше = швидше, але більше пам'яті)")
    args = p.parse_args()

    if not args.video.exists():
        print(f"Файл не знайдено: {args.video}")
        sys.exit(1)

    source = None if args.language.lower() == "auto" else args.language.lower()
    target = args.target.lower()

    # NLLB_LANGS валідуємо лише тоді, коли переклад дійсно знадобиться.
    # Якщо мова вже задана явно (--language) і одразу дорівнює --target,
    # переклад не буде викликаний узагалі — і мова може бути будь-якою,
    # навіть не з таблиці NLLB (режим "лише субтитри").
    if source is not None and source != target:
        if source not in NLLB_LANGS:
            print("Невідома source-мова. Доступні:", ", ".join(sorted(NLLB_LANGS)))
            sys.exit(1)
        if target not in NLLB_LANGS:
            print("Невідома target-мова. Доступні:", ", ".join(sorted(NLLB_LANGS)))
            sys.exit(1)

    setup_cuda_library_path()

    stem = args.video.with_suffix("")
    wav = Path(str(stem) + ".16k.wav")
    txt = Path(str(stem) + f".{target}.txt")
    srt = Path(str(stem) + f".{target}.srt")

    print(f"[1/4] Витягую аудіо: {args.video.name}")
    extract_audio(args.video, wav)

    print("[2/4] Розпізнаю англійську/мову...")
    whisper, device = load_whisper(args.model)
    segments, info = transcribe_audio(whisper, wav, source)

    detected = info.language
    probability = getattr(info, "language_probability", None)
    print(
        f"[Whisper] Визначена мова: {detected}"
        + (f" ({probability:.1%})" if probability is not None else "")
    )

    if source is None:
        source = detected

    original = [s.text.strip() for s in segments]

    if source == target:
        # Мова аудіо вже та, що потрібна -> переклад не викликаємо,
        # просто зберігаємо розпізнаний текст (витяг субтитрів).
        src_name = LANG_NAMES.get(source, source)
        print(f"[3/4] Аудіо вже '{src_name}' ({source}) — переклад пропускаю, лише субтитри.")
        translated = original
    else:
        if source not in NLLB_LANGS:
            print(f"Whisper визначив '{source}', але ця мова не підтримується NLLB для перекладу.")
            print("Доступні мови NLLB:", ", ".join(sorted(NLLB_LANGS)))
            sys.exit(1)
        if target not in NLLB_LANGS:
            print("Невідома target-мова. Доступні:", ", ".join(sorted(NLLB_LANGS)))
            sys.exit(1)
        src_name = LANG_NAMES.get(source, source)
        tgt_name = LANG_NAMES.get(target, target)
        print(f"[3/4] Перекладаю: {src_name} ({source}) -> {tgt_name} ({target})")
        translator = NLLBTranslator(source, target, device)
        translated = translator.translate(original, args.batch_size)

    print("[4/4] Зберігаю результат...")
    txt.write_text("\n".join(translated) + "\n", encoding="utf-8")
    print(f"[OK] TXT: {txt}")

    save_srt(srt, segments, translated)
    print(f"[OK] SRT: {srt}")

    try:
        wav.unlink()
    except OSError:
        pass

    print("[Готово]")


if __name__ == "__main__":
    main()
