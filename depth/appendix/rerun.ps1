# Rebuilds the main results of 11-school-privacy-notices from the frames/sample/notices/codes already on disk.
# NOT run in full (it would re-fetch the web). Safe, fast steps only unless -Fetch is given.
param([switch]$Fetch)
$py = 'D:\Research-Publishing\_tools\biblio-venv\Scripts\python.exe'
$c  = 'D:\Research-Publishing\11-school-privacy-notices\code'
if (-not (Test-Path 'D:\')) { throw 'D: missing' }
if ($Fetch) {
  & $py -I "$c\02_frame_cbse.py"; & $py -I "$c\03_frame_cisce.py"; & $py -I "$c\04_frame_osm.py"; & $py -I "$c\05_frame_edtech.py"
  & $py -I "$c\06_sample.py"; & $py -I "$c\06b_sample_edtech.py"; & $py -I "$c\06c_make_sample_files.py"
  & $py -I "$c\07_collect.py"; & $py -I "$c\07b_render.py"; & $py -I "$c\08_archive.py"
}
# analysis from stored notices and codes (about 1 minute)
& $py -I "$c\06d_enrich.py"
& $py -I "$c\10_autocode.py"
& $py -I "$c\09d_reconcile.py"
& $py -I "$c\11a_reliability.py"
& $py -I "$c\11b_analyse.py"
