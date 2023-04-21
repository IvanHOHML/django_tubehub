#!/usr/bin/env groovy

pipeline {
    agent any
    stages {
        stage('Build'){
            steps{
                echo "Building now ..."
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test'){
            steps{
                echo "Testing now ..."
                sh 'python3 manage.py test song.tests.SongTests'
            }
        }
        stage('Deploy'){
            steps{
                echo "Deploying now ..."
            }
        }
    }
}