"""Patch ipywidgets interactions for headless CI notebook execution."""

import inspect
import os


# Avoid notebook progress widgets during model/data downloads in CI.
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

try:
    import ipywidgets as widgets
except Exception as error:
    print(f"[stub] ipywidgets patch skipped: {error}")
else:

    class _Interact:
        """Replacement for widgets.interact / widgets.interactive.

        Calls the wrapped function once with widget defaults so static outputs are
        captured by nbconvert without requiring a live frontend.
        """

        def __call__(self, *args, **kwargs):
            if len(args) == 1 and callable(args[0]) and not kwargs:
                return self._call_with_defaults(args[0])

            widget_kwargs = kwargs

            def decorator(f):
                return self._call_with_defaults(f, widget_kwargs)

            return decorator

        def _call_with_defaults(self, f, widget_kwargs=None):
            sig = inspect.signature(f)
            call_kwargs = {}

            for name, param in sig.parameters.items():
                widget = (widget_kwargs or {}).get(name)
                if widget is None and param.default is not inspect.Parameter.empty:
                    widget = param.default

                if hasattr(widget, "value"):
                    call_kwargs[name] = widget.value
                elif widget is not None:
                    call_kwargs[name] = widget

            try:
                f(**call_kwargs)
            except Exception as error:
                print(f"[stub] interact call skipped: {error}")

            return f

    widgets.interact = _Interact()
    widgets.interactive = _Interact()

    print("ipywidgets interact patched for headless CI execution")
