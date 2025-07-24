<?php
require_once 'convert_images.php';
require_once 'utils.php';

$files = getHtmlFiles(__DIR__);

foreach ($files as $filepath) {
    $file_basename = basename($filepath);
    echo "Cleaning $file_basename...\n";
    cleanupNestedPictureTags($filepath);
    echo "Finished cleaning $file_basename.\n";
}

echo "All files processed.\n";
?>
