<?php
$pythonPath = "C:/Users/ToQa/AppData/Local/Programs/Python/Python311/python.exe";
define('PhpApiPath', 'http://localhost/api.php');

if (isset($_FILES['image'])) {
    $uploadDirectory = "images/";
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

    if ($fileSize > $maxFileSize) {
        $response = array(
            "success" => false,
            "message" => "File size exceeds the maximum allowed limit."
        );
        echo json_encode($response);
        exit;
    }

    $targetFile = $uploadDirectory . uniqid() . "." . $fileExtension;

    if (move_uploaded_file($fileTmpName, $targetFile)) {
        $imagePath = realpath($targetFile);
        $pythonScript = 'integrationImage.py';

        // استخدم escapeshellarg لتجنب مشاكل المسارات
        $command = escapeshellcmd("$pythonPath $pythonScript " . escapeshellarg($imagePath));
        $output = shell_exec($command);

        if ($output === null) {
            // إذا كان هناك خطأ أثناء تنفيذ سكريبت البايثون
            $response = array(
                "success" => false,
                "message" => "Error executing Python script."
            );
            echo json_encode($response);
            exit;
        }

        $number = trim($output);

        $response = array(
            "stats" => true,
            "number" => $number
        );
        echo json_encode($response);
    } else {
        $response = array(
            "success" => false,
            "message" => "Failed to move the uploaded file."
        );
        echo json_encode($response);
    }
} else {
    $response = array(
        "success" => false,
        "message" => "No image file found in the request."
    );
    echo json_encode($response);
}
?>