from __future__ import annotations

import html
import json

import requests


_REQUEST_TMPL = """\
<div class="api-log-entry" style="margin-bottom:1em;font-family:monospace;">
  <details>
    <summary style="cursor:pointer;font-weight:bold;">{method} {url} &rarr; {status_code}</summary>
    <h4 style="margin:0.5em 0 0.25em;">Request</h4>
    <pre style="background:#f5f5f5;padding:0.5em;overflow:auto;">{request_line}
{request_headers}
{request_body}</pre>
    <h4 style="margin:0.5em 0 0.25em;">Response</h4>
    <pre style="background:#f5f5f5;padding:0.5em;overflow:auto;">HTTP {status_code}
{response_headers}
{response_body}</pre>
  </details>
</div>"""


def _format_headers(headers: dict[str, str]) -> str:
    return "\n".join(f"{k}: {v}" for k, v in headers.items())


def _format_body(body: bytes | str | None) -> str:
    if not body:
        return "(empty)"
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError:
            return "(binary body)"
    if not isinstance(body, str):
        return repr(body)
    try:
        parsed = json.loads(body)
        return json.dumps(parsed, indent=2)
    except (json.JSONDecodeError, TypeError):
        return body


def format_response_as_html(response: requests.Response) -> str:
    req = response.request
    method = req.method or ""
    url = req.url or ""
    request_line = html.escape(f"{method} {url}")
    request_headers = html.escape(_format_headers(dict(req.headers)) if req.headers else "")
    request_body = html.escape(_format_body(req.body))

    response_headers = html.escape(_format_headers(dict(response.headers)))
    response_body = html.escape(_format_body(response.content))

    return _REQUEST_TMPL.format(
        method=html.escape(method),
        url=html.escape(url),
        status_code=response.status_code,
        request_line=request_line,
        request_headers=request_headers,
        request_body=request_body,
        response_headers=response_headers,
        response_body=response_body,
    )
