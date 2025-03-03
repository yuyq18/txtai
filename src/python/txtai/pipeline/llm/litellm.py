"""
LiteLLM module
"""

import os
import contextlib

# Conditional import
try:
    import litellm as api

    LITELLM = True
except ImportError:
    LITELLM = False

from .generation import Generation


class LiteLLM(Generation):
    """
    LiteLLM generative model.
    """

    @staticmethod
    def ismodel(path):
        """
        Checks if path is a LiteLLM model.

        Args:
            path: input path

        Returns:
            True if this is a LiteLLM model, False otherwise
        """

        # pylint: disable=W0702
        if isinstance(path, str) and LITELLM:
            with open(os.devnull, "w", encoding="utf-8") as f, contextlib.redirect_stdout(f):
                try:
                    return api.get_llm_provider(path)
                except:
                    return False

        return False

    def __init__(self, path, template=None, **kwargs):
        super().__init__(path, template, **kwargs)

        if not LITELLM:
            raise ImportError('LiteLLM is not available - install "pipeline" extra to enable')

        # Register prompt template
        self.register(path)

    def execute(self, texts, maxlength, **kwargs):
        results = []
        for text in texts:
            result = api.completion(model=self.path, messages=[{"content": text, "role": "user"}], max_tokens=maxlength, **{**kwargs, **self.kwargs})
            results.append(result["choices"][0]["message"]["content"])

        return results

    def register(self, path):
        """
        Registers a custom prompt template for path.

        Args:
            path: model path
        """

        api.register_prompt_template(model=path, roles={"user": {"pre_message": "", "post_message": ""}})
