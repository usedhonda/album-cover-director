#!/usr/bin/env python3
"""Build a self-contained, labelled concept-selection board without changing artwork."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import json
import os
import tempfile
import warnings
from pathlib import Path

from concept_contract import resolve_asset, validate, validate_review

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:  # pragma: no cover
    Image = None


THUMBNAIL_SIZE = 320
AXIS_LABELS = {
    "title_placement": "タイトルの位置",
    "title_scale": "タイトルの大きさ",
    "figure_role": "人物の役割",
    "camera": "視点",
    "layout": "構図",
    "medium": "表現媒体",
}


class BoardError(Exception):
    def __init__(self, code: str, path: str, message: str):
        self.errors = [{"code": code, "path": path, "message": message}]
        super().__init__(message)


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def same_file(left: Path, right: Path) -> bool:
    if left.resolve() == right.resolve():
        return True
    try:
        return left.samefile(right)
    except (FileNotFoundError, OSError):
        return False


def thumbnail(path: Path, candidate_id: str, minimum_size: int) -> tuple[str, str]:
    """Decode a snapshot, reject non-square sources, and return PNG data plus its hash."""
    if Image is None:
        raise BoardError("pillow-required", str(path), "Pillow is required to build concept previews.")
    try:
        raw = path.read_bytes()
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw)) as opened:
                opened.verify()
            with Image.open(io.BytesIO(raw)) as opened:
                if getattr(opened, "n_frames", 1) != 1:
                    raise BoardError("animated-source", candidate_id, "Use a single still image for each concept preview.")
                if opened.width != opened.height:
                    raise BoardError(
                        "non-square-source", candidate_id,
                        f"Source must be square; got {opened.width}x{opened.height}. The board never crops artwork.",
                    )
                if opened.width < minimum_size:
                    raise BoardError(
                        "preview-below-minimum-size", candidate_id,
                        f"Source is {opened.width}px; this preview contract requires at least {minimum_size}px. Generate an eligible preview before selection.",
                    )
                image = ImageOps.exif_transpose(opened).convert("RGBA")
                image.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.Resampling.LANCZOS)
                encoded = io.BytesIO()
                image.save(encoded, format="PNG", optimize=True)
    except BoardError:
        raise
    except (OSError, ValueError, SyntaxError, UnidentifiedImageError,
            Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise BoardError("image-unreadable", candidate_id, f"Cannot read source image: {path.name}: {exc}") from exc
    data_uri = "data:image/png;base64," + base64.b64encode(encoded.getvalue()).decode("ascii")
    return data_uri, hashlib.sha256(raw).hexdigest()


def note_text(candidate: dict) -> str:
    notes = candidate.get("preview_notes", "")
    if notes is None:
        return ""
    if isinstance(notes, str):
        return notes.strip()
    if isinstance(notes, list) and all(isinstance(note, str) for note in notes):
        return "\n".join(note for note in notes if note.strip())
    raise BoardError("preview-notes-invalid", str(candidate.get("id", "")), "preview_notes must be text or a list of text notes.")


def render_card(candidate: dict, direction: dict, interpretation: dict, data_uri: str) -> str:
    candidate_id = candidate["id"]
    notes = note_text(candidate)
    if not notes:
        notes = "文字の綴り・読みやすさ・細部は未検証です。選択後に確認します。"
    invariants = "".join(f"<li>{escape(item)}</li>" for item in direction["preserve_in_production"])
    axes = "".join(
        f"<dt>{label}</dt><dd>{escape(direction['planned_signature'][key])}</dd>"
        for key, label in AXIS_LABELS.items()
    )
    return f"""<figure class="candidate" data-candidate-id="{escape(candidate_id)}">
  <div class="art"><img src="{data_uri}" width="{THUMBNAIL_SIZE}" height="{THUMBNAIL_SIZE}" alt="候補 {escape(candidate_id)}：{escape(direction['name'])}" decoding="async"></div>
  <figcaption>
    <div class="candidate-heading"><span class="candidate-id">{escape(candidate_id)}</span><h2>{escape(direction['name'])}</h2></div>
    <p class="meaning">{escape(interpretation['summary'])}</p>
    <p class="unverified">コンセプト案・未校了</p>
    <details><summary>表現の仕組み・確認事項</summary>
      <h3>表現の仕組み</h3><p>{escape(direction['visual_mechanism'])}</p>
      <h3>文字・細部の確認事項</h3><p class="notes">{escape(notes)}</p>
      <h3>仕上げでも残すこと</h3><ul>{invariants}</ul>
      <h3>構図の設計</h3><dl>{axes}</dl>
    </details>
  </figcaption>
</figure>"""


def render_document(title: str, cards: list[str], columns: int, draft: bool) -> str:
    if draft:
        status = "内部確認用ドラフト"
        notice = "多様性レビューを必須にせず作った内部確認用です。ユーザーの選択には、レビュー後の比較ボードを使ってください。"
    else:
        status = "選択用コンセプトプレビュー"
        notice = "まず構図と発想を選んでください。タイトルの文字と細部は選択後に仕上げます。"
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="concept-diversity-review" content="{'not-required-internal-draft' if draft else 'passed-hashes-verified'}">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>{escape(title)} — コンセプト比較</title>
<style>
:root {{ color-scheme: light; font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans CJK JP", sans-serif; color: #202420; background: #f4f5f1; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 28px 20px 40px; }}
main {{ max-width: 1120px; margin: 0 auto; }}
header {{ margin-bottom: 22px; }}
.status {{ display: inline-block; margin: 0 0 9px; padding: 5px 10px; border-radius: 5px; background: {'#fce6c9' if draft else '#e0eadf'}; color: #354032; font-size: 12px; font-weight: 700; }}
h1 {{ margin: 0 0 10px; font-size: clamp(24px, 3vw, 34px); line-height: 1.3; overflow-wrap: anywhere; }}
header p {{ margin: 6px 0; max-width: 80ch; line-height: 1.65; font-size: 14px; }}
.notice {{ color: #5c665c; }}
.grid {{ display: grid; grid-template-columns: repeat({columns}, minmax(0, 1fr)); gap: 16px; align-items: start; }}
.candidate {{ margin: 0; min-width: 0; overflow: hidden; border: 1px solid #d9ded6; border-radius: 9px; background: #fff; }}
.art {{ aspect-ratio: 1; background: #ededeb; }}
.art img {{ display: block; width: 100%; height: 100%; object-fit: contain; }}
figcaption {{ padding: 13px 13px 11px; overflow-wrap: anywhere; }}
.candidate-heading {{ display: flex; align-items: baseline; gap: 8px; }}
.candidate-id {{ flex-shrink: 0; padding: 3px 6px; border-radius: 4px; background: #273b31; color: white; font: 700 12px/1.3 ui-monospace, SFMono-Regular, Consolas, monospace; user-select: all; }}
h2 {{ margin: 0; font-size: 15px; line-height: 1.5; }}
.meaning {{ margin: 8px 0; font-size: 13px; line-height: 1.65; }}
.unverified {{ margin: 8px 0 9px; color: #6f766c; font-size: 11px; }}
details {{ border-top: 1px solid #e6e9e2; padding-top: 9px; font-size: 12px; line-height: 1.65; }}
summary {{ cursor: pointer; color: #355341; font-size: 12px; }}
summary:focus-visible {{ outline: 2px solid #355341; outline-offset: 3px; }}
h3 {{ margin: 13px 0 3px; font-size: 12px; }}
details p {{ margin: 3px 0; }}
.notes {{ white-space: pre-line; }}
ul {{ margin: 3px 0; padding-left: 18px; }}
dl {{ display: grid; grid-template-columns: 7em minmax(0, 1fr); gap: 4px 8px; margin: 4px 0; }}
dt {{ color: #697265; }}
dd {{ margin: 0; }}
footer {{ margin-top: 24px; font-size: 12px; color: #6b7467; line-height: 1.7; }}
@media (max-width: 780px) {{ .grid {{ grid-template-columns: repeat({min(columns, 2)}, minmax(0, 1fr)); }} body {{ padding: 20px 14px 32px; }} }}
@media (max-width: 460px) {{ .grid {{ grid-template-columns: 1fr; }} }}
@media print {{ body {{ background: #fff; padding: 0; }} .candidate {{ break-inside: avoid; }} }}
</style>
</head>
<body>
<main>
<header><p class="status">{status}</p><h1>{escape(title)}</h1>
<p>{len(cards)}案を比較できます。気になる案を、画像の下にあるIDで選んでください。複数選べます。</p>
<p class="notice">{notice}</p></header>
<section class="grid" aria-label="コンセプト候補一覧">
{''.join(cards)}
</section>
<footer>選んだIDを伝えると、その案の構図と仕掛けを保って仕上げます。</footer>
</main>
</body>
</html>
"""


def write_atomic(output: Path, content: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, prefix=".concept-board-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def build_board(contract_path: Path, output: Path, columns: int, draft: bool) -> dict:
    contract_path = contract_path.expanduser().resolve()
    output = output.expanduser().resolve()
    if not 1 <= columns <= 4:
        raise BoardError("columns-invalid", "columns", "--columns must be between 1 and 4.")
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BoardError("contract-unreadable", str(contract_path), f"Cannot read run contract: {exc}") from exc
    errors = validate(contract)
    if errors:
        error = BoardError("contract-invalid", str(contract_path), "Run contract is invalid.")
        error.errors = errors
        raise error
    if contract.get("schema_version") != 2 or contract.get("stage") != "concept-preview":
        raise BoardError("concept-stage-required", "stage", "A schema_version 2 concept-preview contract is required.")
    candidates = contract.get("candidates", [])
    if not candidates:
        raise BoardError("candidates-required", "candidates", "The board requires generated candidate images.")
    assets = [(candidate, resolve_asset(contract_path, candidate["output_path"])) for candidate in candidates]
    protected_paths = [contract_path, *(asset for _, asset in assets)]
    if any(same_file(output, protected) for protected in protected_paths):
        raise BoardError("protected-output", str(output), "Output must not overwrite the contract or any source image.")
    if output.suffix.lower() not in {".html", ".htm"}:
        raise BoardError("html-output-required", str(output), "Use an .html or .htm output file.")
    if not draft:
        errors = validate_review(contract, contract_path)
        if errors:
            error = BoardError("review-required", "diversity_review", "Record the visual diversity review before making a selection board; --draft is for internal inspection only.")
            error.errors = errors
            raise error
    directions = {direction["id"]: direction for direction in contract["directions"]}
    interpretations = {item["id"]: item for item in contract["interpretations"]}
    reviewed_hashes = {
        item["id"]: item["sha256"].lower()
        for item in contract.get("diversity_review", {}).get("reviewed_candidates", [])
    } if not draft else {}
    cards = []
    minimum_size = contract["runtime"]["capability_profile"]["preview_minimum_dimension"]
    for candidate, path in assets:
        data_uri, snapshot_hash = thumbnail(path, candidate["id"], minimum_size)
        if not draft and reviewed_hashes.get(candidate["id"]) != snapshot_hash:
            raise BoardError("review-image-changed", candidate["id"], "The source image changed after review. Review the new image before making a selection board.")
        direction = directions[candidate["direction_id"]]
        interpretation = interpretations[direction["interpretation_id"]]
        cards.append(render_card(candidate, direction, interpretation, data_uri))
    document = render_document(contract["release"]["exact_title"], cards, columns, draft)
    write_atomic(output, document)
    return {
        "status": "draft" if draft else "selection-preview",
        "output": str(output),
        "candidates": [candidate["id"] for candidate in candidates],
        "columns": columns,
        "source_images_modified": False,
        "diversity_review_verified": not draft,
        "delivery_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True, help="Schema 2 concept-preview run contract")
    parser.add_argument("--output", type=Path, required=True, help="Self-contained .html board")
    parser.add_argument("--columns", type=int, default=4, help="One to four columns (default: 4)")
    parser.add_argument("--draft", action="store_true", help="Internal inspection only; bypass the recorded diversity review requirement")
    args = parser.parse_args()
    try:
        result = build_board(args.contract, args.output, args.columns, args.draft)
    except BoardError as exc:
        print(json.dumps({"status": "fail", "errors": exc.errors}, ensure_ascii=False, indent=2))
        return 2
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "fail", "errors": [{"code": "board-unreadable", "message": str(exc)}]}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
