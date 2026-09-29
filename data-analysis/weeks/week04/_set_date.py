import json
from pathlib import Path

p = Path(__file__).with_name("structured_data.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
for cell in nb["cells"]:
    if cell.get("id") == "169367f4":
        cell["source"] = [
            "# set trade_date as datetime type\n",
            "df['trade_date'] = pd.to_datetime(df['trade_date'])\n",
        ]
        cell["outputs"] = []
        cell["execution_count"] = None
        break
else:
    raise SystemExit("cell not found")
p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")
