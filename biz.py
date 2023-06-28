import streamlit as st
from PIL import Image
import easyocr
import mysql.connector
import numpy as np


def extract_information(image):
    # Process the image as needed (e.g., resize, crop, enhance)
    processed_image = image

    # Convert the processed image to a NumPy array
    processed_image_np = np.array(processed_image)

    # Perform OCR using easyOCR
    reader = easyocr.Reader(['en'])  # Specify the language
    result = reader.readtext(processed_image_np)

    # Extract relevant information from the OCR result
    extracted_info = {}  # Dictionary to store extracted information
    # Extract and store the relevant information from the OCR result
    # (e.g., company name, card holder name, designation, mobile number, email address, website URL, area, city, state, pin code)

    return extracted_info


# Function to save extracted information and image to the database
def save_to_database(extracted_info, image):
    # Convert the image to bytes
    image_bytes = image.read()

   # Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sreeja1661",
    database="business_cards"
)
mycursor = mydb.cursor()


def extract_information(image):
    # Process the image as needed (e.g., resize, crop, enhance)
    processed_image = image

    # Convert the processed image to a NumPy array
    processed_image_np = np.array(processed_image)

    # Perform OCR using easyOCR
    reader = easyocr.Reader(['en'])  # Specify the language
    result = reader.readtext(processed_image_np)

    # Extract relevant information from the OCR result
    extracted_info = {}  # Dictionary to store extracted information
    # Extract and store the relevant information from the OCR result
    # (e.g., company name, card holder name, designation, mobile number, email address, website URL, area, city, state, pin code)

    return extracted_info


# Function to save extracted information and image to the database
def save_to_database(extracted_info, image):
    # Convert the image to bytes
    image_bytes = image.read()

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@3306",
        database="business_cards"
    )
    mycursor = mydb.cursor()

    # Create a table if it doesn't exist
    mycursor.execute('''CREATE TABLE IF NOT EXISTS business_cards
                     (id INT AUTO_INCREMENT PRIMARY KEY,
                     company_name VARCHAR(255),
                     card_holder_name VARCHAR(255),
                     designation VARCHAR(255),
                     mobile_number VARCHAR(255),
                     email_address VARCHAR(255),
                     website_url VARCHAR(255),
                     area VARCHAR(255),
                     city VARCHAR(255),
                     state VARCHAR(255),
                     pin_code VARCHAR(255))''')

    # Prepare the data to be inserted into the database
    data = (extracted_info['company_name'], extracted_info['card_holder_name'], extracted_info['designation'],
            extracted_info['mobile_number'], extracted_info['email_address'], extracted_info['website_url'],
            extracted_info['area'], extracted_info['city'], extracted_info['state'], extracted_info['pin_code'])

    # Insert the data into the database
    mycursor.execute('INSERT INTO business_cards VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', data)

    # Commit the changes and close the database connection
    mydb.commit()
    mydb.close()


# Main function to run the Streamlit application
def main():
    # Set the title and sidebar layout
    st.title("BizCardX: Extracting Business Card Data")
    st.sidebar.title("Menu")

    # Add functionality to the sidebar menu
    menu_options = ["Upload Business Card", "View Database"]
    selected_menu = st.sidebar.selectbox("Select an option", menu_options)

    # Handle selected menu options
    if selected_menu == "Upload Business Card":
        st.header("Upload Business Card")

        # Create a file uploader widget
        uploaded_file = st.file_uploader("Upload an image of the business card", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Open and display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Business Card", use_column_width=True)

            # Extract information from the image
            extracted_info = extract_information(image)

            # Display the extracted information
            st.subheader("Extracted Information")
            for key, value in extracted_info.items():
                st.write(f"{key}: {value}")

            # Save the extracted information and image to the database
            if st.button("Save to Database"):
                save_to_database(extracted_info, uploaded_file)
                st.success("Data saved successfully!")

    elif selected_menu == "View Database":
        st.header("View Database")

        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@3306",
            database="business_cards"
        )
        mycursor = mydb.cursor()

        # Fetch all the data from the database
        mycursor.execute("SELECT * FROM business_cards")
        data = mycursor.fetchall()

        # Display the data in a table
        if len(data) > 0:
            st.dataframe(data, columns=['ID', 'Company Name', 'Card Holder Name', 'Designation',
                                        'Mobile Number', 'Email Address', 'Website URL',
                                        'Area', 'City', 'State', 'Pin Code'],
                         width=800, height=600)
        else:
            st.warning("No data found in the database.")

        # Close the database connection
        mydb.close()


# Run the main function
if __name__ == '__main__':
    main()
