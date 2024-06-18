<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

define('SERVER_PATH', 'http://localhost/mahmoud/');
define('AI_PATH', 'C:/xampp/htdocs/mahmoud/integrationImage.py');
$pythonPath = "C:/Users/ToQa/AppData/Local/Programs/Python/Python311/python.exe";

if (isset($_FILES['image'])) {
    echo "File uploaded.\n";
    $uploadDirectory = __DIR__ . "/images/";
    $allowedExtensions = array("jpg", "jpeg", "png", "gif");
    $maxFileSize = 10 * 1024 * 1024;

    $fileName = $_FILES["image"]["name"];
    $fileSize = $_FILES["image"]["size"];
    $fileTmpName = $_FILES["image"]["tmp_name"];
    $fileType = $_FILES["image"]["type"];
    $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

    if (!in_array($fileExtension, $allowedExtensions)) {
        $response = array(
            "success" => false,
            "message" => "Invalid file type. Only JPG, JPEG, PNG, and GIF files are allowed."
        );
        echo json_encode($response);
        exit;
    }
    echo "File extension checked.\n";

    if ($fileSize > $maxFileSize) {
        $response = array(
            "success" => false,
            "message" => "File size exceeds the maximum allowed limit."
        );
        echo json_encode($response);
        exit;
    }
    echo "File size checked.\n";

    $targetFile = $uploadDirectory . uniqid() . "." . $fileExtension;

    if (!move_uploaded_file($fileTmpName, $targetFile)) {
        $response = array(
            "success" => false,
            "message" => "Failed to move uploaded file."
        );
        echo json_encode($response);
        exit;
    }
    echo "File moved to upload directory.\n";

    $fullImagePath = SERVER_PATH . "images/" . basename($targetFile);

    // Call the Python script with the local image path as a command-line argument
    $pythonOutput = shell_exec("$pythonPath " . AI_PATH . " " . escapeshellarg($targetFile) . " 2>&1");

    // Print the output from the Python script
    echo "Python script executed. Output: " . $pythonOutput;
} else {
    $response = array(
        "success" => false,
        "message" => "Failed to upload image."
    );
    echo json_encode($response);
}
?>