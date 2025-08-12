# Progress

This file tracks the project's progress using a task list format.
2023-11-14 12:00:00 - Log of updates made.
2023-11-15 12:00:00 - Updated with image downloading functionality.

*

## Completed Tasks

* Created the main `PhDExamDownloader` class with core functionality
* Implemented methods to scrape the main page and find exam page links
* Added functionality to extract PDF URLs from iframes
* Implemented PDF download functionality with error handling
* Created a command-line interface for customization
* Added unit tests to verify functionality
* Created a batch file for Windows users
* Added comprehensive documentation in README.md
* Enhanced downloader to detect and download embedded images from iframes and divs
* Added functionality to organize images in dedicated subfolders
* Updated CLI and README to reflect new image downloading capabilities

* Implemented robust PDF filename generation and sanitization to prevent invalid filename errors
* Added fallback mechanisms for filename generation (Content-Disposition, URL, page URL, UUID)

* Debugged and resolved the "response variable not defined" error in `download_pdf`
* Added `.gitignore` file to ignore the `exams/` directory

## Current Tasks

## Next Steps

* Potential improvements to error handling
* Enhance image quality and format detection
* Consider adding a graphical user interface
* Add support for other similar websites
* Implement parallel downloading for better performance
* Add option to filter content types (PDFs only, images only, or both)