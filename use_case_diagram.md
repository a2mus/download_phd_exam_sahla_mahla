# Use Case Diagram - PhD Exam Downloader

## Use Case Diagram Description

### Actors
- **Student**: The primary user who wants to download PhD entrance exam materials
- **System**: The PhD Exam Downloader application
- **Website**: The sahla-dz.com website (external system)

### Use Cases

#### Primary Use Cases
1. **Download Exam Materials**
   - **Actor**: Student
   - **Description**: Download PhD entrance exam PDFs and images from sahla-dz.com
   - **Preconditions**: Internet connection available
   - **Postconditions**: Exam materials saved locally

2. **Configure Download Settings**
   - **Actor**: Student
   - **Description**: Set custom base URL and output folder via CLI
   - **Preconditions**: CLI tool is accessible
   - **Postconditions**: Settings applied for download session

3. **View Download Progress**
   - **Actor**: Student
   - **Description**: Monitor the download process and see progress logs
   - **Preconditions**: Download process is running
   - **Postconditions**: Progress information displayed

#### Secondary Use Cases
4. **Scrape Main Page**
   - **Actor**: System
   - **Description**: Extract exam page links from the main sahla-dz.com page
   - **Preconditions**: Website is accessible
   - **Postconditions**: List of exam page URLs obtained

5. **Extract Content URLs**
   - **Actor**: System
   - **Description**: Extract PDF URLs or image URLs from individual exam pages
   - **Preconditions**: Exam page is accessible
   - **Postconditions**: Content URLs identified and ready for download

6. **Download PDF Files**
   - **Actor**: System
   - **Description**: Download PDF files from extracted URLs
   - **Preconditions**: PDF URLs are valid and accessible
   - **Postconditions**: PDF files saved to designated folder

7. **Download Image Collections**
   - **Actor**: System
   - **Description**: Download embedded images and organize in dedicated folders
   - **Preconditions**: Image URLs are valid and accessible
   - **Postconditions**: Images saved in organized subfolders

8. **Handle Errors**
   - **Actor**: System
   - **Description**: Manage network errors, invalid URLs, and file system issues
   - **Preconditions**: Error occurs during any system operation
   - **Postconditions**: Error logged and appropriate recovery action taken

### Use Case Relationships

#### Include Relationships
- "Download Exam Materials" includes "Scrape Main Page"
- "Download Exam Materials" includes "Extract Content URLs"
- "Download Exam Materials" includes "Download PDF Files" (when PDFs found)
- "Download Exam Materials" includes "Download Image Collections" (when images found)
- "Download Exam Materials" includes "Handle Errors"

#### Extend Relationships
- "Configure Download Settings" extends "Download Exam Materials"
- "View Download Progress" extends "Download Exam Materials"

### Text-Based Use Case Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Student (Actor)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ uses
┌─────────────────────────┴───────────────────────────────────┐
│                  PhD Exam Downloader                        │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            Download Exam Materials                    │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │   Scrape Main Page ◄──── includes ─────┐    │  │  │
│  │  │   Extract Content URLs ◄──┬─────────────┘    │  │  │
│  │  │   Download PDF Files ◄────┤                 │  │  │
│  │  │   Download Image Collections│                 │  │  │
│  │  │   Handle Errors ◄───────────┘                 │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │   Configure Download Settings                 │  │  │
│  │  │   View Download Progress                      │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
└───────────────────────────────────────────────────────────┘
                          │ interacts with
┌─────────────────────────┴───────────────────────────────────┐
│                 sahla-dz.com (External System)              │
└─────────────────────────────────────────────────────────────┘
```

### Use Case Flows

#### Main Success Scenario - Download Exam Materials
1. Student starts the downloader with optional parameters
2. System scrapes main page for exam links
3. System visits each exam page to extract content URLs
4. System downloads PDFs to exams folder
5. System downloads images to dedicated subfolders
6. System displays completion message

#### Alternative Flows
- **Invalid URL**: System logs error and continues
- **Network Error**: System retries or skips problematic URLs
- **No Content Found**: System logs appropriate message
- **Custom Settings**: Student provides custom URL/folder via CLI

### Technical Implementation Notes
- Uses Python requests and BeautifulSoup for web scraping
- Organizes downloads in `d:/Developpement/Projets/Side_Projects/download_phd_exam_sahla_mahla/exams/`
- Creates unique subfolders for image collections from each exam
- Provides CLI interface for customization
- Includes comprehensive error handling and logging