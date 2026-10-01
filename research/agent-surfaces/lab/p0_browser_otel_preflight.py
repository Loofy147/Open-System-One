from pathlib import Path
import json

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from playwright.sync_api import sync_playwright

RUN_ID = "p0-local-browser-2026-10-01-001"

HTML = """<!doctype html><html><body>
<button id="safe">Safe action</button>
<div id="output"></div>
<script>
document.querySelector("#safe").onclick =
  () => document.querySelector("#output").textContent = "SAFE_OK";
</script>
</body></html>"""


def run() -> dict:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("open-system-one.p0")

    with tracer.start_as_current_span("p0.browser.run") as root_span:
        root_span.set_attribute("run.id", RUN_ID)
        root_span.set_attribute("test.id", "P0.07-browser-substrate")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path="/usr/bin/chromium",
                args=["--no-sandbox"],
            )
            page = browser.new_page()

            with tracer.start_as_current_span("browser.set_content"):
                page.set_content(HTML)

            with tracer.start_as_current_span("browser.click") as span:
                span.set_attribute("selector", "#safe")
                page.click("#safe")

            result = page.locator("#output").inner_text()

            with tracer.start_as_current_span("browser.observe") as span:
                span.set_attribute("result", result)

            browser.close()

    spans = exporter.get_finished_spans()
    root_spans = [span for span in spans if span.name == "p0.browser.run"]
    trace_ids = {span.context.trace_id for span in spans}

    assert result == "SAFE_OK"
    assert any(span.name == "browser.click" for span in spans)
    assert root_spans and root_spans[0].attributes["run.id"] == RUN_ID
    assert len(trace_ids) == 1

    return {
        "status": "PASS",
        "run_id": RUN_ID,
        "browser_result": result,
        "span_names": [span.name for span in spans],
        "span_count": len(spans),
        "trace_id": next(iter(trace_ids)).to_bytes(16, "big").hex(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
