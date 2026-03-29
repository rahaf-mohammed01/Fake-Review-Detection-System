# Fake Review Detection System

## Overview
This project is a Natural Language Processing (NLP)-based system developed to detect fake and misleading product reviews. It analyzes textual data and applies machine learning techniques to classify reviews as genuine or fake.

## Features
- Text preprocessing (cleaning, normalization, filtering)
- Feature extraction using TF-IDF
- Machine learning-based classification
- Detection of fake and misleading reviews
- Model evaluation and comparison

## Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Natural Language Processing (NLP)

## How It Works
1. Load and clean the dataset  
2. Normalize text (remove URLs, punctuation, etc.)  
3. Convert text into numerical features using TF-IDF  
4. Train machine learning models  
5. Evaluate performance and select the best model  
6. Classify reviews as fake or real  

## Model
The system uses the following machine learning models:
- Logistic Regression  
- Support Vector Machine (SVM)  

SVM achieved the best performance and was selected as the final model.

## Results
- Logistic Regression Accuracy: ~93.5%  
- SVM Accuracy: ~94.4%  
- SVM achieved the highest F1-score and overall performance  

