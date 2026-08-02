
import subprocess
from pathlib import Path
import scan

def sort(dir):
   for file in dir.iterdir():
      if file.suffix == '.dmg':
         sign = subprocess.run(
           ['codesign', '-dvv', str(file)],
           capture_output=True, text=True,timeout=20)

         def verification(string):
             fold_path = dir / 'Downloaded DMGs' / string
             fold_path.mkdir(exist_ok=True)
             print(fold_path)
             file.rename(fold_path / file.name)
         if sign.returncode == 0:
             verification('Signed')
         else:
             verification('Unsigned')



dir = Path('~/Downloads')
dir = dir.expanduser()
print(dir)

if '__main__' == __name__:
    sort(dir)
    scan.create_process()
    scan.log()
    scan.runtime()



