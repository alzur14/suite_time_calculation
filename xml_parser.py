import pathlib
import xml.etree.ElementTree as ET


def format_time(seconds):
    if seconds >= 60:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes} m. {secs} s."
    else:
        return f"{seconds:.1f} s."


folder = pathlib.Path(".")

results = []
for file_path in folder.glob("*.xml"):
    root = ET.parse(file_path).getroot()
    name = root.attrib.get("name")
    time = root.attrib.get("time")
    if name and time:
        results.append({"name": name, "time": float(time)})
        
results.sort(key=lambda x: x["time"], reverse=True)


with open("result.json", "w") as res:
    for r in results:
        res.write(f'{{"name": "{r["name"]}", "time": "{format_time(r["time"])}"}},\n')