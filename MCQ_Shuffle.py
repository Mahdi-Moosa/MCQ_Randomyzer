import os
import random
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Image
from reportlab.lib.enums import TA_CENTER

def randomize_mcq_options(mcq_list):
    """
    Randomizes the options for multiple-choice questions (MCQs).

    Args:
        mcq_list (list): A list of MCQs.

    Returns:
        list: A list of randomized MCQ options.
    """
    for mcq in mcq_list:
        options = [option[1] for option in mcq['options']]
        random.shuffle(options)
        mcq['options'] = list(zip(sorted([option[0] for option in mcq['options']]), options))
    return mcq_list

def save_as_pdf(output_file, story):
    # Save the generated story as a PDF file
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    doc.build(story)
    
def read_boilerplate_text(boilerplate_file):
    # Read and process the boilerplate text from a file

    try:
        with open(boilerplate_file, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.replace('\n', '<br/>')  # Replace line breaks with HTML tags
            text = text.replace('<left>', '<div style="text-align: left;">').replace('</left>', '</div>')  # Replace <left> tags with appropriate HTML tags for left alignment
            text = text.replace('<right>', '<div style="text-align: right;">').replace('</right>', '</div>')  # Replace <right> tags with appropriate HTML tags for right alignment
            text = text.replace('[B]', '<b>').replace('[/B]', '</b>')  # Replace [B] tags with HTML tags for bold formatting
            return text
    except FileNotFoundError:
        print(f"Error: Boilerplate file '{boilerplate_file}' not found.")
        return None


def main():
    if os.path.isfile("input.txt"):
        file_name = "input.txt"
    else:
        file_name = input("Enter the name of the file containing the questions and answer options: ")

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return

    mcq_list = []
    current_mcq = None
    
    # Ask for user input to determine if MCQs should be randomized
    valid_yes_answers = ['Y', 'YES']
    valid_no_answers = ['N', 'NO']
    randomize_mcqs_input = None
    
    while randomize_mcqs_input not in valid_yes_answers and randomize_mcqs_input not in valid_no_answers:
        randomize_mcqs_input = input("Do you want to randomize the MCQs? (Y/N): ").upper()

    for line in lines:
        line = line.replace("\t", " ") # Replace tabs with spaces
        if line.startswith("Q"):
            if current_mcq:
                mcq_list.append(current_mcq)
            question_number = re.search(r"\d+", line).group()  # Extract the question number from the line
            question_text = re.sub(r"Q\d+\.\s*", "", line)  # Remove the question number from the line
            current_mcq = {'question': question_text, 'options': []}
        else:
            match = re.match(r"^([a-z])\. (.*)$", line)  # Match option labels and text
            if match:
                option_label = match.group(1)
                option_text = match.group(2)
                current_mcq['options'].append((option_label, option_text))

    if current_mcq:
        mcq_list.append(current_mcq)

    num_question_sets = int(input("Enter the number of randomized question sets to generate: "))

    output_file = "shuffled_output.pdf"
    story = []

    # Define custom styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontSize=16, textColor=colors.blue)
    paragraph_style = ParagraphStyle('ParagraphStyle', parent=styles['Normal'])
    question_style = ParagraphStyle('QuestionStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.black)
    option_style = ParagraphStyle('OptionStyle', parent=styles['BodyText'], fontSize=12, textColor=colors.black, spaceAfter=12)  # Adjust the value as per your preference

    # Define custom style for center-aligned text
    center_style = ParagraphStyle('CenterStyle', parent=styles['BodyText'], alignment=TA_CENTER)
    
    # Add image
    image_path = "set_image.jpg"
    if os.path.isfile(image_path):
        image = Image(image_path, width=100, height=100)
        
    # Read boilerplate text from file or ask user
    boilerplate_file = "boilerplate.txt"
    boilerplate_text = read_boilerplate_text(boilerplate_file)
    if boilerplate_text is None:
        boilerplate_file = input("Enter the name of the file containing the boilerplate text: ")
        boilerplate_text = read_boilerplate_text(boilerplate_file)
        if boilerplate_text is None:
            return
    
    # Create boilerplate paragraph
    boilerplate_paragraph = Paragraph(boilerplate_text, paragraph_style)

    for i in range(num_question_sets):
        randomized_mcqs = randomize_mcq_options(mcq_list)
        
        # Randomize question-answer group order if requested by the user
        if randomize_mcqs_input in valid_yes_answers:
            random.shuffle(randomized_mcqs)
        
        # Add image and boilerplate text before each question set
        if os.path.isfile(image_path):
            story.append(image)
        story.append(Paragraph(f"<b>Total marks: 5; Time: 6 minutes </b>", center_style))
        story.append(boilerplate_paragraph)

        # Add title(s)
        story.append(Paragraph(f"<b>Set {i + 1}</b>", title_style))

        for j, mcq in enumerate(randomized_mcqs, 1):
            question_text = re.sub(r'^Q\d+:', '', mcq['question'])  # Remove "Q" followed by number from the question text
            story.append(Paragraph(f"<b>{j}. {question_text}</b>", question_style))

            for k, option in enumerate(mcq['options'], 1):
                option_label, option_text = option
                option_paragraph = Paragraph(f"{option_label}. {option_text}", option_style)
                story.append(option_paragraph)

            # Add page break after each question set
            if j >= len(randomized_mcqs):
                story.append(PageBreak())

    save_as_pdf(output_file, story)
    print(f"Shuffled MCQ options saved to '{output_file}'.")

if __name__ == "__main__":
    main()
