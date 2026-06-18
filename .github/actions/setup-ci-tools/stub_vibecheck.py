"""Disable Vibecheck feedback widgets during headless CI execution."""

try:
    import vibecheck
except Exception as error:
    print(f"[stub] vibecheck patch skipped: {error}")
else:

    def _render_noop(self, *args, **kwargs):
        print("[stub] vibecheck render skipped for headless CI execution")
        return None

    if hasattr(vibecheck, "DatatopsContentReviewContainer"):
        vibecheck.DatatopsContentReviewContainer.render = _render_noop
        print("vibecheck render patched for headless CI execution")
