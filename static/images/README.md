# Image Assets

This folder mirrors the paths referenced in `/data/*.json`. Drop real photos in here
using the exact filenames already referenced, and every placeholder box on the site
will automatically start showing the real photo instead — no template code needs to
change.

## Folder map

```
static/images/
  branding/     NCC crest, Indian Navy crest, Indian flag graphic (used in the hero)
  officers/     ANO/CTO, CO, Group Commander, DG NCC portraits
  achievers/    Achiever portraits (data/achievers.json)
  alumni/       Batch group photos (data/alumni.json)
  gallery/
    ncc/        NCC activity photos (camps, boat pulling, firing, drill)
    community/  Community service photos (blood donation, cleanliness drives, plantation)
```

## Using a GitHub repository for images

Since the plan is to host images in a separate GitHub repository (useful once the
photo library gets large), two options work well with this Flask structure:

**Option A — Git submodule / clone into `static/images`**
Clone or add the image repository as a git submodule at `static/images/`, keeping the
same folder names and filenames referenced in the JSON files under `/data`. Nothing
else in the app needs to change.

**Option B — Point at raw GitHub URLs directly**
Replace the `src` values in `data/gallery.json` (and the `photo` values in the other
JSON files) with the raw content URL for each image, e.g.:

```
https://raw.githubusercontent.com/<your-org>/<images-repo>/main/gallery/ncc/2026_catc_01.jpg
```

Flask does not need to serve the file itself in that case — the browser loads it
straight from GitHub. This keeps the website repository light and lets non-technical
volunteers upload new photos straight to the images repository.

## Filename convention already used in the data files

`<year>_<event-short-name>_<sequence>.jpg`, e.g. `2026_catc_01.jpg`. Keeping this
convention makes it easy to batch-upload a year's photos at once.
