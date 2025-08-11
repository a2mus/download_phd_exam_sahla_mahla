# Decision Log

This file records architectural and implementation decisions using a list format.
2023-11-14 12:00:00 - Log of updates made.
2023-11-15 12:00:00 - Added decision for image downloading functionality.

*

## Decision

* Use a class-based approach for the downloader implementation
* Implement a separate command-line interface script
* Use BeautifulSoup for HTML parsing
* Add unit tests with mocking for testability
* Extend downloader to handle embedded images in iframes and divs
* Organize images from each exam in dedicated subfolders

## Rationale 

* Class-based approach provides better organization and encapsulation of functionality
* Separate CLI script allows for more flexibility in how the tool is used
* BeautifulSoup is a robust and well-maintained library for HTML parsing
* Unit tests with mocking allow testing without making actual network requests
* Supporting embedded images ensures comprehensive exam content collection
* Dedicated subfolders for images maintain organization and prevent filename conflicts

## Implementation Details

* Created a `PhDExamDownloader` class with methods for each step of the process
* Used regular expressions to extract PDF URLs from iframe src attributes
* Implemented error handling throughout the codebase
* Added a batch file for Windows users to simplify execution
* Modified `extract_pdf_url_from_iframe` to detect content type (PDF or images)
* Added a new `download_images` method to handle image downloading and organization
* Updated the `run` method to process both PDFs and images
* Set default destination folder to the specified exams directory