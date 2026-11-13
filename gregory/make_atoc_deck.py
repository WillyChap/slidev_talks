"""Write gregory-atoc.md (ATOC 4870 theme) from gregory/atoc_template.md, copying the speaker notes
from gregory-lecture.md so both decks share one set of notes. Run from the project root."""
import re
notes = re.findall(r"<!--(.*?)-->", open("gregory-lecture.md").read(), flags=re.S)
assert len(notes) == 12, len(notes)
s = open("gregory/atoc_template.md").read()
for i, n in enumerate(notes, 1):
    s = s.replace("{{NOTE%d}}" % i, n.strip())
assert "{{NOTE" not in s
open("gregory-atoc.md", "w").write(s)
print("wrote gregory-atoc.md")
