# Predictive Maintenance System & Anomaly Detection

img

---
## Overview

Modern industries lose billions due to unplanned equipment failures . This project builds a Predictive Maintenance System that detects anomalies in Amazon ec2 request latency system using Deep Learning & Anomaly Detection.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [How This Works](#how-this-works)
- [Why Built](#why-this-is-built)

## Features

- **Real-time Anomaly Detection** – Detects faults before system failures.
- **Autoencoder + LSTM Hybrid** – Uses two models for robust detection.
- **Visualized Alerts** – Red dots mark potential failures in the graph.
- **API-Based Architecture** – Upload sensor data via Flask API & get predictions.

## Tech Stack

- **Machine Learning:** Tensorflow, LSTM, Autoencoder, Python
- **Backend:** Flask
- **Frontend:** React.js

## Setup & Installation

### Run Locally

1. Clone Repo

```
git clone https://github.com/GeenethMedagedara/Predictive_Maintenance_System.git
cd predictive-maintenance
```

2. Install Dependencies

```
pip install -r requirements.txt

# Go to frontend directory
cd frontend
npm install
```

3. Train the model

Run the two notebooks data_exploration.ipynb and modeling.ipynb respectively 

img

4. Run the App
```
# To run react app
cd frontend 
npm run dev

# To run flask backend
cd backend
flask run --host=0.0.0.0 --port=4000
```

5. Access the frontend at
```
http://localhost:8080
```

## How This Works

> Long Short-Term Memory (LSTM) is a type of Recurrent Neural Network (RNN) designed to handle sequential data and long-term dependencies.
> Unlike standard RNNs, LSTMs can retain information over long time steps because it (Prevent Vanishing Gradient).

> Autoencoders are unsupervised neural networks used for feature compression and anomaly detection.
> This compresses the input into lower-dimensional representation and then reconstructs the input from the compressed data.
> If this compression error is high it is considered an anomaly.

In this project I mainly used a hybrid approach by first training the LSTM model on non-anomalized data and then later using an anomalized dataset to predict the diviational differences from the trained dataset. And then using a threshold value to detect the anomalized data while combining the predictions of the autoencoders as well to increase the accuracy of the predictions. And then a graph is plotted along with the predicted values.

The user has to input the dataset according to the criteria given in the react frontend and the flask backend uses the models to predict the anomaly values and plots the values on a graph

## Why This is Built

I built this project to gain an understanding of how to work with time series data and use LSTMs to predict future EC2 request latencies and also learn how to train an unsupervised model to detect unusual system behavior (Autoencoder).
