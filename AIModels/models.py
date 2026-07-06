import ctypes
import llama_cpp
from llama_cpp import Llama

LOG_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_void_p
)(lambda *_: None)
llama_cpp.llama_log_set(LOG_CALLBACK, ctypes.c_void_p())


class LLM:
    def __init__(
        self,
        model_path,
        n_ctx=4096,
        n_gpu_layers=10,
        flash_attn=True,
        verbose=False,
        chat_format=None,
        **kwargs
    ):
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            flash_attn=flash_attn,
            verbose=verbose,
            chat_format=chat_format,
            **kwargs
        )

    def generate(self, messages, stream=False, **kwargs):
        res = self.llm.create_chat_completion(
            messages=messages,
            stream=stream,
            **kwargs
        )
        if stream:
            return res
        return res["choices"][0]["message"]["content"]
