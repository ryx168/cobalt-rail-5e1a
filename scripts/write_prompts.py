#!/usr/bin/env python3
"""Write prompts/<slot>.txt for every AI shot slot in shots.json.

The style block is the Seedance-2.0 cinematic look from Min Choi's clip
(x.com/minchoi/status/2021322290076520607), transposed from a rain-soaked
cyberpunk duel to the Orient Express crossing Xinjiang: anamorphic, 2.39:1,
teal shadows and warm practicals, mist, one recurring heroine, a train as the
co-star. Each prompt is self-contained so any image or video model can take it.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
cfg = json.loads((HERE / "shots.json").read_text(encoding="utf-8"))
HER = cfg["heroine"]

STYLE = (
    "Cinematic still frame from a prestige travel film, live-action photoreal. "
    "Widescreen 2.39:1 composition inside a 16:9 frame, anamorphic lens with soft "
    "blue-green halation, shallow depth of field, gentle film grain. Colour grade: "
    "cold teal shadows, warm amber highlights, desaturated mid-tones, subtle haze "
    "and drifting mist. Natural light only. No text, no captions, no watermark, "
    "no logo, no subtitles, no extra people unless named. "
)

TRAIN = ("The train is the third-generation New Orient Express luxury tourist train: "
         "deep blue and cream livery with a gold stripe, large panoramic windows, "
         "warm lamplight inside. ")

SHOTS = {
 "01_window_dawn": (
    f"{HER}, close-up, seen from inside a luxury train compartment at dawn. She rests her "
    "temple against the panoramic window, eyes half open, breath fogging the glass; outside, "
    "the Gobi desert slides past in pale blue pre-dawn light with the snow line of the Tianshan "
    "range on the horizon. Warm reading lamp on the walnut panelling behind her. Slow push-in."),
 "02_train_tianshan": (
    TRAIN + "Very wide aerial shot at first light: the train crosses a vast grey-green steppe on a "
    "single track, a thin plume of mist trailing, the snow-capped Tianshan mountains filling the "
    "background, low sun raking across the grass, the train small in the landscape."),
 "03_tianchi": (
    f"Heavenly Lake (Tianchi) in the Tianshan mountains. {HER} stands alone on a wooden lakeside "
    "walkway, camel coat pulled tight, looking out over the dark jade lake toward Bogda Peak's "
    "glacier; spruce forest on the slopes, thin morning mist on the water, a single reflection. "
    "Wide shot from behind, she is small against the mountain."),
 "04_turpan": (
    f"Turpan grape valley. {HER} walks under a long trellis tunnel of green vines heavy with grapes, "
    "dappled hard sunlight, dust in the air, an elderly Uyghur farmer in a doppa cap offering a bunch "
    "of grapes in the background, mud-brick walls. Medium shot, backlit, lens flare."),
 "05_sugong": (
    "The Emin Minaret (Sugong Tower) in Turpan at golden hour: a tall tapering mud-brick minaret with "
    "geometric brick patterns beside a flat-roofed mosque, Flaming Mountains red in the far haze, "
    "heat shimmer, dramatic low angle looking up, long shadows, no people."),
 "06_kashgar_window": (
    f"Kashgar old town. An ochre mud-plaster wall with two carved turquoise wooden windows; {HER} "
    "leans out of one window smiling softly, afternoon light, a local child peeking from the other. "
    "Flat frontal composition, warm orange wall, teal window frames."),
 "07_kashgar_faces": (
    "Three young Uyghur women in embroidered velvet coats and tall round hats, laughing and shielding "
    "their eyes from the sun, in front of a rough adobe wall in Kashgar; the Id Kah mosque's yellow "
    "facade soft in the background. Medium close-up, handheld energy, warm light."),
 "08_baishahu": (
    "White Sand Lake (Baishahu) on the Karakoram Highway: a turquoise-milk lake under bone-white sand "
    "dunes and dark Kunlun peaks, a ribbon of asphalt in the foreground, blue sky with high cirrus, "
    f"and {HER} standing at the roadside guardrail with her coat blown by the wind. Ultra-wide."),
 "09_panlong": (
    "Panlong Ancient Road: a mountain road of 639 hairpin bends coiling like a dragon down a bare "
    "ochre mountainside on the Pamir plateau, seen from directly above at dawn, tiny seven-seat "
    "vehicles on the switchbacks, long blue shadows in every bend, snow on the far ridges."),
 "10_karakul": (
    f"Karakul Lake with Muztagh Ata, the 'father of ice mountains', rising behind: a mirror-still "
    f"alpine lake, {HER} crouched at the shore touching the water, a Kyrgyz yurt and two Bactrian "
    "camels at the left, the huge white glaciated dome of the mountain reflected. Golden hour, wide."),
 "11_kizil": (
    "The Kizil Thousand Buddha Caves near Kuqa: honeycombed cave openings cut into a pale cliff above "
    "a row of green poplars, the bronze statue of the monk Kumarajiva seated in front, late light "
    "glowing on the rock, the Muzart river valley behind. Slow upward tilt framing."),
 "12_canyon": (
    f"Tianshan Mysterious Grand Canyon in Kuqa: narrow slot canyon of deep red sandstone, walls "
    f"twisting upward, a sliver of blue sky at the top, {HER} walking away from camera into the "
    "glowing red passage, dust motes in a shaft of light. Low angle, warm red-orange with teal sky."),
 "13_bosten": (
    "Bosten Lake wetlands at Korla: a vast shallow lake edged with golden autumn reeds, hundreds of "
    "swans and wild ducks taking off at once, their wings catching low sun, mist over the water, "
    "distant blue mountains. Wide, telephoto compression, flocks mid-flight."),
 "14_hemu_dawn": (
    f"Hemu village at dawn: Tuvan log cabins in a mountain basin, woodsmoke rising straight up into "
    f"cold air, white birch forest turning gold on the slopes, {HER} on a wooden viewing platform "
    "wrapped in her coat with a steaming cup, first sun hitting the ridge. Wide, misty, serene."),
 "15_kanas": (
    "Kanas Lake in the Altai mountains: the Moon Bay bend of a milky turquoise river seen from "
    "above, dense larch and spruce forest in autumn gold and green on both banks, mist lifting off "
    "the water, snow peaks far behind. Aerial wide, slow drift."),
 "16_wucaitan": (
    "Wucaitan 'Five Coloured Beach' at Burqin: a rainbow-striped yardang cliff of red, orange, "
    "yellow and purple rock above the blue Irtysh river, green poplar forest on the far bank, "
    f"sunset side light making the colours glow, {HER} as a tiny figure on the boardwalk."),
 "17_platform_night": (
    TRAIN + f"Night at a station platform in Xinjiang. {HER} walks away from camera along the wet "
    "platform toward the lit train, her reflection in the puddles, steam drifting, warm window "
    "lights in a long row, cold blue night sky, a conductor in uniform waiting at an open door. "
    "Low angle from behind, slow dolly follow; the mood of a film's closing shot."),
 "18_title_plate": (
    TRAIN + "Dark atmospheric plate for a title card: the train's front at night in light rain, "
    "headlamp glowing through mist, deep blue and black with amber window light, lots of empty "
    "dark space in the centre of the frame for text, cinematic, moody."),
}

out = HERE / "prompts"
out.mkdir(exist_ok=True)
for slot, body in SHOTS.items():
    (out / f"{slot}.txt").write_text(STYLE + body + "\n", encoding="utf-8")
slots = {s["slot"] for s in cfg["segments"] if s.get("slot")}
missing = slots - set(SHOTS)
print(f"wrote {len(SHOTS)} prompts; slots without a prompt: {sorted(missing) or 'none'}")
