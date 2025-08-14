<?php require_once 'config.php'; ?>
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Smart Knowledge Hub</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; }
    .card { border: 1px solid #e5e7eb; padding: 16px; border-radius: 12px; margin-bottom: 16px; }
    input, textarea { width: 100%; padding: 8px; margin-top: 6px; }
    button { padding: 10px 16px; border-radius: 10px; border: 1px solid #111827; background: #111827; color: white; cursor: pointer; }
    .muted { color: #6b7280; font-size: 12px; }
    pre { white-space: pre-wrap; background: #f3f4f6; padding: 12px; border-radius: 8px; }
  </style>
</head>
<body>
  <h1>Smart Knowledge Hub & Workflow Agent</h1>

  <div class="card">
    <h3>Ask a question</h3>
    <form method="POST" action="send.php">
      <label>Message</label>
      <textarea name="message" rows="3" required placeholder="e.g., What are your business hours?"></textarea>
      <div style="margin-top: 10px;">
        <button type="submit">Send</button>
      </div>
    </form>
    <p class="muted">This calls FastAPI /chat which runs a LangGraph workflow and returns an answer (DB-backed for FAQs).</p>
  </div>

  <div class="card">
    <h3>Upload a file (CSV or PDF)</h3>
    <form method="POST" action="upload.php" enctype="multipart/form-data">
      <label>Note (optional)</label>
      <input type="text" name="note" placeholder="Describe what this file is">
      <label style="margin-top: 8px;">File</label>
      <input type="file" name="file" required accept=".csv,application/pdf">
      <div style="margin-top: 10px;">
        <button type="submit">Upload</button>
      </div>
    </form>
    <p class="muted">This calls FastAPI /upload which sends the file through MCP tools (parse_csv / extract_pdf_text).</p>
  </div>
</body>
</html>
