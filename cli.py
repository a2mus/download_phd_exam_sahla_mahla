import os
import argparse
from download_exams import PhDExamDownloader

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Download PhD exam content (PDFs and images) from sahla-dz.com')
    
    # Add arguments
    parser.add_argument('--url', type=str, 
                        default="https://lmd.sahla-dz.com/sujets-concours-doctorat-informatique/",
                        help='Base URL containing links to exam pages')
    
    parser.add_argument('--output', type=str,
                        default="d:/Developpement/Projets/Side_Projects/download_phd_exam_sahla_mahla/exams/",
                        help='Destination folder to save PDFs and images')
    
    parser.add_argument('--no-selenium', action='store_true',
                        help='Disable Selenium WebDriver (use only requests for static content)')
    
    # Parse arguments
    args = parser.parse_args()
    
    use_selenium = not args.no_selenium
    
    print(f"Base URL: {args.url}")
    print(f"Output folder: {args.output}")
    print(f"Using Selenium for lazy-loaded content: {use_selenium}")
    
    # Create and run the downloader
    downloader = PhDExamDownloader(args.url, args.output, use_selenium=use_selenium)
    downloader.run()

if __name__ == "__main__":
    main()