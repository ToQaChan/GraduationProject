<?php
define('SERVER_PATH', 'http://localhost/mahmoud/');
define('AI_PATH', 'C:/xampp/htdocs/mahmoud/integration.py');

if (isset($_POST['prediction'])) {
    $prediction = $_POST['prediction'];
    $response = array(
        "success" => true,
        "message" => "Prediction received successfully."
    );
    echo json_encode($response);
    exit;
}

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
        $fullImagePath = __DIR__ . '/' . $targetFile;

        // Pass the image file path to the Python script
        $command = escapeshellcmd("python " . AI_PATH . " " . $fullImagePath . " 2>&1");
        $pythonResponse = shell_exec($command);

        if ($pythonResponse) {
            $decodedResponse = json_decode($pythonResponse, true);
            if ($decodedResponse) {
                $response = array(
                    "success" => "success",
                    "message" => "Image uploaded successfully.",
                    "image_url" => $fullImagePath,
                    "python_response" => $decodedResponse
                );
            } else {
                $response = array(
                    "success" => "failed",
                    "message" => "Failed to parse Python response.",
                    "python_output" => $pythonResponse  // Print the output from the Python script
                );
            }
        } else {
            $response = array(
                "success" => "failed",
                "message" => "No response from Python script."
            );
        }

        echo json_encode($response);
    } else {
        $response = array(
            "success" => "failed",
            "message" => "Failed to upload image."
        );
        echo json_encode($response);
    }
} else {
    $response = array(
        "success" => "failed",
        "message" => "No image received."
    );
    echo json_encode($response);
}
?>