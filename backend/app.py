import os
))


@app.get('/api/health')
def health():
return {"status": "ok"}


@app.post('/api/categorize')
def categorize():
data = request.get_json(force=True)
txns = data.get('transactions', [])
descriptions = [t.get('description', '') for t in txns]
preds = categorizer.predict(descriptions)
for t, cat in zip(txns, preds):
t['category'] = str(cat)
return jsonify({"transactions": txns})


@app.post('/api/upload')
def upload():
if 'file' not in request.files:
return jsonify({"error": "file is required"}), 400
f = request.files['file']
try:
if f.filename.lower().endswith('.csv'):
df = pd.read_csv(f)
else:
return jsonify({"error": "Only CSV supported in this sample"}), 400
except Exception as e:
return jsonify({"error": f"Failed to parse CSV: {e}"}), 400


# normalize columns
cols = {c.lower().strip(): c for c in df.columns}
# Expect at least description & amount; date optional
desc_col = cols.get('description') or cols.get('details') or list(df.columns)[1]
amount_col = cols.get('amount') or list(df.columns)[2]
date_col = cols.get('date') if 'date' in cols else None


records = []
for _, row in df.iterrows():
desc = str(row.get(desc_col, '')).strip()
amt = float(row.get(amount_col, 0) or 0)
if date_col:
try:
dt = dateparser.parse(str(row.get(date_col)))
except Exception:
dt = datetime.utcnow()
else:
dt = datetime.utcnow()
records.append({"date": dt.isoformat()[:10], "description": desc, "amount": amt})


# categorize
preds = categorizer.predict([r['description'] for r in records])
for r, cat in zip(records, preds):
r['category'] = str(cat)


# persist
with engine.begin() as conn:
for r in records:
conn.execute(text(
"INSERT INTO transactions(date, description, amount, category) VALUES (:date, :description, :amount, :category)"
), r)


return jsonify({"count": len(records)})


@app.get('/api/transactions')
def list_transactions():
with engine.begin() as conn:
res = conn.execute(text("SELECT id, date, description, amount, category FROM transactions ORDER BY date DESC, id DESC"))
rows = [dict(r._mapping) for r in res]
return jsonify({"transactions": rows})


@app.get('/api/summary')
def summary():
with engine.begin() as conn:
res = conn.execute(text("SELECT category, ROUND(SUM(amount),2) as total FROM transactions GROUP BY category ORDER BY total DESC"))
rows = [dict(r._mapping) for r in res]
return jsonify({"byCategory": rows})


if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)