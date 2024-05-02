# HAM: Streamlit-Based Personal Assistant

HAM is a personal assistant application developed with Streamlit, leveraging several Python libraries to provide functionalities like voice recognition, text-to-speech, and web operations. It can perform tasks such as searching Wikipedia, opening web pages, playing music, and providing real-time responses through voice.

## Features

- Voice activated commands for various tasks.
- Integration with Wikipedia for information search.
- Capability to open websites like YouTube and Google.
- Music playback from a specified directory.
- Custom movie database interaction through speech commands.
- Real-time speech-to-text display and processing.

## Prerequisites

Before you start, ensure you have the following installed:
- Python 3.8 or higher
- `pip` for Python package management

## Installation

Follow these steps to set up the assistant:

### Step 1: Clone the Repository

Clone the GitHub repository to your local machine using:

```bash
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install streamlit pyttsx3 wikipedia webbrowser pandas speech_recognition difflib
```

### Step 3: Environment Setup

Ensure you have a working microphone set up as the default recording device, as the application uses speech recognition.

### Step 4: Running the Application

To run the application, use the following command in your terminal:

```bash
streamlit run app.py
```

This will start the Streamlit server and the application will be accessible through a web browser at the URL provided by Streamlit (typically `http://localhost:8501`).

## Usage

After launching the application, click the "Listen 🎙️" button to start voice commands. You can ask HAM to perform various tasks such as:

- "Search Wikipedia for [topic]"
- "Open YouTube"
- "Play music"
- "What's the time?"
- "Open my GitHub"

The assistant will process your voice input and perform the requested action.
