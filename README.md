# Sentiment Analysis on Borobudur Temple Reviews from TripAdvisor

This repository contains the code and data for my bachelor thesis on sentiment analysis of reviews of Borobudur Temple, sourced from TripAdvisor. The primary aim of this project is to evaluate tourist sentiments (positive, negative, neutral) using Support Vector Machine (SVM) as the classification method. By analyzing these reviews, we aim to gain insights into visitors' perceptions of Borobudur Temple and its related tourist experiences.

## Introduction
This project focuses on performing sentiment analysis on user reviews of Borobudur Temple collected from TripAdvisor. The sentiment classification uses SVM to categorize reviews into positive, negative, or neutral sentiments. We also include aspect-based sentiment analysis to understand different facets of tourism experiences by filtering specific aspects using expert-validated keywords.

## Data Collection
The data was scraped from the [TripAdvisor Borobudur Temple page](https://www.tripadvisor.com/Attraction_Review-g790291-d320054-Reviews-Borobudur_Temple-Borobudur_Magelang_Central_Java_Java.html) on **24 May 2024**. Only English-language reviews were collected for analysis to evaluate tourist perceptions and satisfaction levels.


## Text Preprocessing
The raw text data underwent several preprocessing steps:
- **Text Cleaning:** Removal of unwanted characters and symbols.
- **Case Folding:** Converting all text to lowercase for consistency.
- **Tokenization:** Splitting the text into individual words (tokens).
- **Stopword Removal:** Removing common words (e.g., "and", "the") that don't carry significant meaning.
- **Stemming:** Reducing words to their base form (e.g., "running" to "run").

## Data Annotation
The collected review data was manually labeled by an annotator into three categories: **Positive**, **Negative**, and **Neutral**.

## Feature Extraction
We used **Term Frequency-Inverse Document Frequency (TF-IDF)** to convert the preprocessed text data into numerical feature vectors suitable for SVM model training.

## Model Training & Evaluation
An **SVM (Support Vector Machine)** model was trained on the extracted features to classify the sentiments of the reviews. The model's performance was evaluated using standard classification metrics such as accuracy, precision, recall, and F1-score.

## Aspect Filtering
In addition to general sentiment analysis, we performed aspect-based filtering using keywords related to various aspects (Attraction, Image, Human Resource, Amenities, Accessibility, Price). These keywords were validated by an expert in tourism studies to ensure accuracy in categorizing sentiments specific to each aspect.

## Results & Visualization
The results of the sentiment analysis, including visualizations, can be found [here](#https://borobudursa.streamlit.app/). These visualizations help provide a clear understanding of the overall sentiment distribution and tourist satisfaction for different aspects of the temple.

## Research Details
For a more detailed explanation of the methodology, results, and conclusions, you can refer to the full thesis document available at the following link: [http://repository.upi.edu/id/eprint/122805](http://repository.upi.edu/id/eprint/122805)
