# 新東方快車 南北疆專列 — cinematic trailer (tour 7620)

A ~90 s trailer for XO Tours' 2027 Orient Express Xinjiang rail tour, rendered
entirely on GitHub Actions. The look is borrowed from the Seedance 2.0 clip in
[Min Choi's post](https://x.com/minchoi/status/2021322290076520607): 2.39:1
letterbox, anamorphic teal-and-amber grade, mist, one recurring heroine, a
slow open and an escalating montage. Here the co-star is the train and the
duel is replaced by thirteen days of Xinjiang.

## How it renders

| step | script | needs |
|---|---|---|
| prompts | `scripts/write_prompts.py` | nothing; writes `prompts/<slot>.txt` |
| AI stills (optional) | `scripts/gen_stills.py` | repo secrets `CF_ACCOUNT_ID`, `CF_API_TOKEN` (Workers AI flux-1-schnell) |
| AI clips (optional) | `scripts/gen_clips.py --route seedance\|fal` | secret `ARK_API_KEY` (BytePlus ModelArk, Seedance) or `FAL_KEY` (Kling) |
| music | `scripts/make_bgm.py` | nothing; a synthesised royalty-free bed. Or pass `bgm_url` to the workflow |
| build | `scripts/build_trailer.py` | ffmpeg + Noto CJK fonts (the workflow installs both) |
| QA | `scripts/review_frames.py` | makes `out/review.jpg`, attached to the release |

Per shot slot, the builder takes the first that exists:
`shots/<slot>/clip.mp4` → `shots/<slot>/generated.png` → the tour photo named in
`shots.json`. So the zero-key run already produces a complete trailer from the
tour's own brochure photos with Ken Burns moves, and every key you add upgrades
shots without touching the edit.

## Run it

Push to `main`, or dispatch by hand:

```
gh workflow run render.yml -R ryx168/cobalt-rail-5e1a -f stills=ai -f clips=seedance -f quality=final
```

Outputs: an artifact `trailer-7620-<run>` and a release `run-<n>` with
`trailer_7620.mp4` and `review.jpg`.

## Keys

Set them as repository secrets (Settings → Secrets → Actions), never in the repo:

- `CF_ACCOUNT_ID` + `CF_API_TOKEN` (token with Workers AI read/run) → AI stills
- `ARK_API_KEY` → Seedance image-to-video; put the Seedance 2.0 model id in the
  repository variable `ARK_VIDEO_MODEL` once your account lists it (the script's
  default is `seedance-1-0-pro-250528`)
- `FAL_KEY` → Kling image-to-video through fal.ai

The clip routes were written from the public API docs and have not been run
here (no key was available at build time); expect to fix a field name on the
first real run.

## Edit

`shots.json` is the edit: order, duration, Ken Burns move, caption and source
per segment. `scripts/write_prompts.py` holds the per-shot prompt text; the
`heroine` string in `shots.json` keeps her consistent across shots. Captions
are Traditional Chinese; prompts are English so any model takes them.

## Local check

```
pip install numpy pillow
python scripts/write_prompts.py
python scripts/make_bgm.py
set TRAILER_FONT=C:/Windows/Fonts/msjh.ttc
set TRAILER_FONT_BOLD=C:/Windows/Fonts/msjhbd.ttc
python scripts/build_trailer.py --quality draft
python scripts/review_frames.py out/trailer_7620_draft.mp4
```

## Photos

`stills/` are XO Tours' own tour-7620 brochure photos (supplier material already
published on xotours.net). The music bed is synthesised, so the zero-key output
is safe to publish.
