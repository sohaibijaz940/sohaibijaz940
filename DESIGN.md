# Profile artwork maintenance

Palette: charcoal/ivory/muted lime, with warm-ivory light alternatives. The header is an original GIF with a fixed headline and three rotating learning/building lines; PNG counterparts are selected by the README picture elements for reduced motion. Project cards use actual application captures and link to source code, not an unconfigured public demo.

Evidence counts describe current repository content (four demos, six stories, four explainers). Update them when that scope changes. Skills are separated from learning goals. No hardcoded streak or contribution count is used.

The daily activity workflow fetches GitHub's contributionCalendar, tests its streak calculation, generates static metrics/calendars and runs a revision-pinned Platane/snk action in a read-only generation job. A separate repository-scoped publish job writes only assets/generated. It uses GitHub's automatic workflow token; no personal token or paid service is needed. Generated commits use github-actions[bot], not the account owner's authorship. Failure to retrieve real data fails the job rather than fabricating statistics.

Statistics cover the reported rolling twelve-month calendar. A current streak may be counted through yesterday when today is empty. The longest streak is limited to that window; it is not claimed as an all-time record. Update timestamps are embedded in the actual artwork.

To regenerate design images on Windows, use the saved render_profile.py source (Python/Pillow, Arial and Georgia fonts) under design/. It reads interface captures from a locally configured portfolio folder. This renderer is optional; normal profile maintenance does not need to run it. Generated SVGs contain no external script or font dependencies.
