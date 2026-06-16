<?php
// utils.php

/**
 * Recursively finds all HTML files in a directory.
 *
 * @param string $dir The directory to search.
 * @return array An array of file paths.
 */
function getHtmlFiles($dir) {
    $files = [];
    $iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS));
    foreach ($iterator as $file) {
        if ($file->isFile() && strtolower($file->getExtension()) == 'html') {
            $files[] = $file->getPathname();
        }
    }
    return $files;
}
