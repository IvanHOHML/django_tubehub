#!/usr/bin/env groovy

pipeline {
    agent any
    stages {
        stage('Build'){
            echo "Building now ..."
            "
            sh 'make'
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            "
        }
        stage('Test'){
            echo "Testing now ..."
            "
            sh 'make check || true'
            junit '**/target/*.xml'
            "
        }
        stage('Deploy'){
            echo "Deploying now ..."
        }
    }
}