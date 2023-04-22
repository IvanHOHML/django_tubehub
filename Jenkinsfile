#!/usr/bin/env groovy

pipeline {
    agent {
        label 'docker'
    }
    stages {
        stage('Build'){
            agent {
                label 'docker'
                image 'python:3.9'
            }
            steps{
                echo "Building now ..."
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test'){
            agent {
                label 'docker'
                image 'python:3.9'
            }
            steps{
                echo "Testing now ..."
                sh 'python3 manage.py test song.tests.SongTests'
            }
        }
        stage('Deploy'){
            agent {
                label 'docker'
                image 'python:3.9'
            }
            steps{
                echo "Deploying now ..."
            }
        }
    }
}

