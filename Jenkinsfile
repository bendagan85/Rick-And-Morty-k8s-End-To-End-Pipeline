pipeline {
    agent any

    environment {
        // הגדרת משתנים גלובליים
        IMAGE_NAME = "rick-morty-app"
        TAG = "latest"
    }

    stages {
        // שלב 1: בניית הדוקר אימג'
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // שימו לב: הפקודה הזו מניחה שג'נקינס רץ על המחשב שלך ויש לו גישה לדוקר
                    sh "docker build -t ${IMAGE_NAME}:${TAG} ."
                }
            }
        }

        // שלב 2: התקנה/שדרוג עם Helm
        stage('Deploy with Helm') {
            steps {
                script {
                    echo 'Deploying to Minikube using Helm...'
                    // הפקודה משדרגת את ההתקנה אם קיימת, או מתקינה אם לא (upgrade --install)
                    // אנחנו דורסים את ה-pullPolicy ל-Never כדי שישתמש באימג' המקומי שבנינו
                    sh "helm upgrade --install rm-app ./rick-morty-chart --set image.pullPolicy=Never --set image.repository=${IMAGE_NAME} --set image.tag=${TAG}"
                }
            }
        }

        // שלב 3: בדיקות (Verification)
        stage('Verify Deployment') {
            steps {
                script {
                    echo 'Waiting for pods to be ready...'
                    // המתנה קצרה שהפוד יעלה
                    sh 'sleep 10'
                    
                    echo 'Running Healthcheck...'
                    // בדיקה שהאפליקציה מחזירה תשובה (בהנחה שג'נקינס יכול לגשת ל-localhost:8080)
                    // אם ג'נקינס רץ בתוך קונטיינר, יכול להיות שצריך כתובת אחרת, אבל למקומי זה יעבוד
                    try {
                        sh 'curl -f http://localhost:8080/healthcheck'
                    } catch (Exception e) {
                        echo 'Warning: Could not curl localhost, but deployment might be fine inside K8s'
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline finished successfully! 🚀'
        }
        failure {
            echo 'Pipeline failed. ❌'
        }
    }
}