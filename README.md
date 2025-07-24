# Image and HTML Cleanup Scripts

This document provides instructions for using the PHP scripts to clean and maintain the HTML files in this project.

## Overview

There are two main scripts:

1.  `convert_images.php`: This script contains the core logic for cleaning up nested `<picture>` tags within HTML files. It uses PHP's DOMDocument to parse the HTML and safely remove any `<picture>` elements found inside another `<picture>` element, which can cause rendering issues.

2.  `run_cleanup.php`: This is the runner script that iterates through a predefined list of all HTML files in the project and executes the cleanup function from `convert_images.php` on each file.

## Usage

To run the cleanup process on all HTML files, execute the `run_cleanup.php` script from the command line using the PHP executable in your XAMPP installation.

### Steps:

1.  Open a terminal or command prompt.
2.  Navigate to the project's root directory:
    ```sh
    cd c:\xampp\htdocs\signageworks.in
    ```
3.  Run the script:
    ```sh
    c:\xampp\php\php.exe run_cleanup.php
    ```

The script will process each file listed in `run_cleanup.php` and print its progress to the console. The process is complete when the script finishes execution.
