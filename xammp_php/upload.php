<?php
require_once 'config.php';
if (!isset($_FILES['file'])) { http_response_code(400); echo "File required"; exit; }

$note = isset($_POST['note']) ? $_POST['note'] : '';

$boundary = uniqid();
$delimiter = '--------------------------' . $boundary;

$post_data = '';
function add_string($name, $value) {
  global $post_data, $delimiter;
  $post_data .= "--$delimiter\r\n";
  $post_data .= 'Content-Disposition: form-data; name="' . $name . "\"\r\n\r\n" . $value . "\r\n";
}
function add_file($name, $filename, $mime, $content) {
  global $post_data, $delimiter;
  $post_data .= "--$delimiter\r\n";
  $post_data .= 'Content-Disposition: form-data; name="' . $name . '"; filename="' . $filename . "\"\r\n";
  $post_data .= 'Content-Type: ' . $mime . "\r\n\r\n";
  $post_data .= $content . "\r\n";
}

$file_tmp = $_FILES['file']['tmp_name'];
$file_name = $_FILES['file']['name'];
$file_type = $_FILES['file']['type'];
$file_content = file_get_contents($file_tmp);

add_string('note', $note);
add_file('file', $file_name, $file_type, $file_content);
$post_data .= "--$delimiter--\r\n";

$ch = curl_init("$API_BASE/upload");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
  'Content-Type: multipart/form-data; boundary=' . $delimiter,
  'Content-Length: ' . strlen($post_data)
]);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
$res = curl_exec($ch);
curl_close($ch);

header('Content-Type: text/html; charset=utf-8');
echo "<a href='index.php'>&larr; Back</a>";
echo "<h2>Upload Result</h2>";
echo "<pre>" . htmlspecialchars($res) . "</pre>";
