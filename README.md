# MCQ Randomizer

A script to randomize multiple-choice question (MCQ) options and generate a PDF with shuffled questions and options.

## Prerequisites

- Python 3.6 or higher

## Usage

* Prepare a text file (input.txt) containing the questions and answer options in the following format:


      Q1. Question 1
      a. Option A
      b. Option B
      c. Option C
      d. Option D
      Q2. Question 2
      a. Option A
      b. Option B
      c. Option C
      d. Option D

* Each question should start with "Q" followed by a number. Options should be listed with lowercase letters as labels (a, b, c, d).

* Prepare a text file (boilerplate.txt) containing the boilerplate text to be included before each question set in the generated PDF. Customize the formatting and content of the boilerplate text as needed.

* Run the script:

```bash

    python mcq_randomizer.py
```

* If the input.txt or boilerplate.txt files are not found in the project directory, the script will prompt you to enter the respective file names.
* When prompted, specify whether you want to randomize the MCQs by entering either "Y" or "N".
* Enter the number of randomized question sets to generate.

* The shuffled MCQ options will be saved as a PDF file (shuffled_output.pdf) in the project directory.

## Customization

* Modify the input.txt file to add your own questions and options.
* Modify the set_image.jpg to add your own logo.
* Customize the formatting and styling of the generated PDF by modifying the appropriate styles in the script.
* To include an image before each question set, place an image file named set_image.jpg in the project directory.
* Customize the boilerplate text by modifying the boilerplate.txt file. The script will read the text from this file and include it before each question set in the generated PDF.
