# Video Recommendation Engine

A sophisticated recommendation system that suggests personalized video content based on user preferences and engagement patterns using deep neural networks. Ref: to see what kind of motivational content you have to recommend, take reference from our Empowerverse App [ANDROID](https://play.google.com/store/apps/details?id=com.empowerverse.app) || [iOS](https://apps.apple.com/us/app/empowerverse/id6449552284).

## 🌟 Project Overview

This project implements a video recommendation algorithm that:

- Delivers personalized content recommendations
- Handles cold start problems using mood-based recommendations
- Utilizes deep neural networks for content analysis
- Integrates with external APIs for data collection
- Implements efficient data caching and pagination

## 🛠️ Technology Stack

- **Backend Framework**: Flask
- **Database**: PostgreSQL
- **Caching**: Redis
- **Task Queue**: Celery
- **Documentation**: Swagger/OpenAPI

## 🗉️ Prerequisites

- Virtual environment (recommended)
- PostgreSQL and Redis installed
The recommendation engine uses a Deep Neural Network (DNN) architecture with the following components:

1. **Data Preprocessing**
   - Feature engineering
   - Data normalization
   - Missing value handling
   - Categorical encoding
2. **Model Architecture**
   - Embedding layers for categorical features
   - Dense layers with ReLU activation
   - Dropout for regularization
   - Output layer with appropriate activation
3. **Cold Start Handling**
   - Mood-based initial recommendations
   - Content-based filtering fallback
   - Popularity-based recommendations
