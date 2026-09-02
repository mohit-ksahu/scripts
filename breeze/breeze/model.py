import ctypes
import queue
import random
import threading
from pathlib import Path
import numpy as np

from breeze._native import Callback, Error, Native, Request
from breeze.audio import Audio, Chunk, load_audio

class Model:

    def __init__(self, path, use_gpu=True, lib_path=None):
        location = Path(path).resolve()
        if not location.is_file():
            raise FileNotFoundError(f"Model file not found: {location}")
        self._path = str(location)
        self._native = Native(lib_path)
        self._lock = threading.Lock()
        self._context = self._native.library.breeze_init(
            self._path.encode("utf-8"),
            1 if use_gpu else 0,
        )
        if not self._context:
            error = self._native.get_error()
            raise Error(f"Failed to load model from {self._path}: {error}")
        self._rate = self._native.library.breeze_sample_rate(self._context)

    @property
    def rate(self):
        return self._rate

    @property
    def path(self):
        return self._path

    def _prepare(
        self,
        text,
        instruction=None,
        ref_audio=None,
        ref_text=None,
        cfg_scale=1.0,
        seed=None,
        max_new_tokens=0,
        split_chars=0,
        temperature=0.0,
        top_k=0,
        top_p=0.0,
        repetition_penalty=0.0,
    ):
        if not text:
            raise ValueError("Input 'text' cannot be empty.")
        if ref_audio is not None and not ref_text:
            raise ValueError("'ref_text' is required when 'ref_audio' is provided.")
        if ref_text and ref_audio is None:
            raise ValueError("'ref_audio' is required when 'ref_text' is provided.")
        request = Request()
        request.text = text.encode("utf-8")
        request.instruction = (instruction or "Speak clearly and naturally.").encode("utf-8")
        request.ref_text = ref_text.encode("utf-8") if ref_text else None
        request.cfg_scale = float(cfg_scale)
        request.seed = int(random.randint(0, 2147483647) if seed is None else seed)
        request.max_new_tokens = int(max_new_tokens)
        request.split_chars = int(split_chars)
        request.temperature = float(temperature)
        request.top_k = int(top_k)
        request.top_p = float(top_p)
        request.repetition_penalty = float(repetition_penalty)
        reference_data = None
        if ref_audio is not None:
            if isinstance(ref_audio, (str, Path)):
                array = load_audio(ref_audio, rate=self._rate)
            elif isinstance(ref_audio, Audio):
                array = ref_audio.samples
            else:
                array = np.asarray(ref_audio, dtype=np.float32)
            reference_data = np.ascontiguousarray(array, dtype=np.float32)
            request.ref_audio = reference_data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            request.ref_audio_len = len(reference_data)
        return request, reference_data

    def generate(
        self,
        text,
        instruction=None,
        ref_audio=None,
        ref_text=None,
        cfg_scale=1.0,
        seed=None,
        max_new_tokens=0,
        split_chars=0,
        temperature=0.0,
        top_k=0,
        top_p=0.0,
        repetition_penalty=0.0,
        on_chunk=None,
    ):
        if not self._context:
            raise Error("Model is closed.")
        request, reference_data = self._prepare(
            text=text,
            instruction=instruction,
            ref_audio=ref_audio,
            ref_text=ref_text,
            cfg_scale=cfg_scale,
            seed=seed,
            max_new_tokens=max_new_tokens,
            split_chars=split_chars,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
        )
        chunks = []
        index = 0

        def callback(pointer, count, _user):
            nonlocal index
            chunk_data = np.ctypeslib.as_array(pointer, shape=(count,)).copy()
            chunks.append(chunk_data)
            if on_chunk is not None:
                chunk = Chunk(chunk_data, self._rate, index)
                index += 1
                if on_chunk(chunk) is False:
                    return 1
            return 0

        callback_handle = Callback(callback)
        with self._lock:
            status = self._native.library.breeze_generate(
                self._context,
                ctypes.byref(request),
                callback_handle,
                None,
            )
        del reference_data
        del callback_handle
        if status != 0:
            error = self._native.get_error()
            raise Error(f"Generation failed: {error}")
        samples = np.concatenate(chunks) if chunks else np.empty(0, dtype=np.float32)
        return Audio(samples, self._rate)

    def stream(
        self,
        text,
        instruction=None,
        ref_audio=None,
        ref_text=None,
        cfg_scale=1.0,
        seed=None,
        max_new_tokens=0,
        split_chars=0,
        temperature=0.0,
        top_k=0,
        top_p=0.0,
        repetition_penalty=0.0,
    ):
        channel = queue.Queue()
        errors = []

        def worker():
            try:
                self.generate(
                    text=text,
                    instruction=instruction,
                    ref_audio=ref_audio,
                    ref_text=ref_text,
                    cfg_scale=cfg_scale,
                    seed=seed,
                    max_new_tokens=max_new_tokens,
                    split_chars=split_chars,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty,
                    on_chunk=lambda chunk: channel.put(chunk),
                )
            except Exception as error:
                errors.append(error)
            finally:
                channel.put(None)

        thread = threading.Thread(target=worker)
        thread.start()
        while True:
            item = channel.get()
            if item is None:
                break
            yield item
        thread.join()
        if errors:
            raise errors[0]

    def close(self):
        with self._lock:
            if self._context:
                self._native.library.breeze_free(self._context)
                self._context = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __del__(self):
        self.close()

    def __repr__(self):
        return f"<Model path='{self._path}' rate={self._rate}Hz>"

def load(path, use_gpu=True, lib_path=None):
    return Model(path=path, use_gpu=use_gpu, lib_path=lib_path)