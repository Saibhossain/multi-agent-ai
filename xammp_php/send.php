<?php
require_once 'config.php';
if (!isset($_POST['message'])) { http_response_code(400); echo "Message required"; exit; }
$msg = $_POST['message'];

$payload = json_encode(['message' => $msg]);

$ch = curl_init("$API_BASE/chat");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
$res = curl_exec($ch);
curl_close($ch);

header('Content-Type: text/html; charset=utf-8');
echo "<a href='index.php'>&larr; Back</a>";
echo "<h2>Chat Response</h2>";
echo "<pre>" . htmlspecialchars($res) . "</pre>";
