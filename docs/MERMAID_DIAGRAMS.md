# 📊 Mermaid Architecture Diagrams

This document contains interactive Mermaid diagrams for the Uruguay Climate Change Monitoring & AI Analysis System. These diagrams render beautifully on GitHub, GitLab, and many documentation platforms.

---

## 🎯 High-Level System Architecture

```mermaid
graph TB
    subgraph "USER LAYER"
        Browser["🌐 Browser<br/>(Chrome, Firefox)"]
        Mobile["📱 Mobile App<br/>(Future)"]
        CLI["⌨️ CLI Tools<br/>(Scripts)"]
    end

    subgraph "PRESENTATION LAYER"
        subgraph "React Frontend :3000"
            Dashboard["📊 Dashboard"]
            MLPred["🤖 ML Predictions"]
            AIInsights["💡 AI Insights"]
            ClimateCharts["📈 Climate Charts"]
            AlertMgmt["🚨 Alert Management"]
            Stats["📉 Statistics"]
        end
    end

    subgraph "APPLICATION LAYER"
        subgraph "Flask Backend :5000"
            subgraph "API Routes"
                DataAPI["/api/data"]
                MLAPI["/api/ml"]
                AIAPI["/api/ai"]
                AlertsAPI["/api/alerts"]
                GeminiCyodaAPI["/api/gemini-cyoda"]
            end

            subgraph "Services"
                DataService["DataService"]
                MLService["MLService"]
                GeminiService["GeminiService"]
                AlertService["AlertService"]
                IntegrationService["IntegrationService"]
            end
        end
    end

    subgraph "ML ENGINE"
        LSTM["🧠 LSTM Model<br/>(Keras)"]
        Prophet["📊 Prophet<br/>(Facebook)"]
        Anomaly["🔍 Anomaly Detector<br/>(IsoForest)"]
        Classifier["🎯 XGBoost/LightGBM<br/>Classifier"]
    end

    subgraph "AI ENGINE"
        Gemini["✨ Google Gemini<br/>1.5 Flash"]
    end

    subgraph "MCP CLIENT"
        CyodaMCP["🔗 Cyoda MCP SDK"]
    end

    subgraph "DATA LAYER"
        CSV["📄 CSV Files"]
        Models["💾 Trained Models<br/>(.keras, .pkl)"]
    end

    Browser -->|HTTPS| Dashboard
    Mobile -->|HTTPS| Dashboard
    CLI -->|HTTPS| Dashboard

    Dashboard -->|REST API| DataAPI
    MLPred -->|REST API| MLAPI
    AIInsights -->|REST API| AIAPI
    AlertMgmt -->|REST API| AlertsAPI

    DataAPI --> DataService
    MLAPI --> MLService
    AIAPI --> GeminiService
    AlertsAPI --> AlertService
    GeminiCyodaAPI --> IntegrationService

    DataService --> CSV
    MLService --> LSTM
    MLService --> Prophet
    MLService --> Anomaly
    MLService --> Classifier

    LSTM --> Models
    Prophet --> Models
    Anomaly --> Models
    Classifier --> Models

    GeminiService --> Gemini
    AlertService --> CyodaMCP
    IntegrationService --> Gemini
    IntegrationService --> CyodaMCP

    style Browser fill:#e1f5ff
    style Mobile fill:#e1f5ff
    style CLI fill:#e1f5ff
    style Dashboard fill:#fff3e0
    style Gemini fill:#f3e5f5
    style CyodaMCP fill:#e8f5e9
    style LSTM fill:#ffe0b2
    style Prophet fill:#ffe0b2
```

---

## 🔄 Data Flow: Gemini + Cyoda Integration

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React Frontend<br/>(Dashboard)
    participant Backend as Flask Backend<br/>(gemini_cyoda_routes)
    participant Gemini as Gemini Service<br/>(AI Analysis)
    participant GeminiAPI as Google Gemini<br/>1.5 Flash
    participant Alert as Alert Service
    participant Cyoda as Cyoda MCP<br/>Platform

    User->>Frontend: Clicks "Analyze Weather"
    activate Frontend
    Frontend->>Backend: POST /api/gemini-cyoda/analyze<br/>{temp: 0.1, location: "Uruguay", date: "2025-10-24"}
    activate Backend

    Backend->>Gemini: analyze_climate_data(0.1°C)
    activate Gemini
    Gemini->>GeminiAPI: Send analysis prompt
    activate GeminiAPI
    GeminiAPI-->>Gemini: {severity: "high", analysis: "...", recommendations: [...]}
    deactivate GeminiAPI
    Gemini-->>Backend: AI Analysis Result
    deactivate Gemini

    Backend->>Backend: Format alert data
    Backend->>Alert: create_alert(alert_data)
    activate Alert
    Alert->>Cyoda: mcp__cyoda__entity_create_entity_tool()
    activate Cyoda
    Cyoda-->>Alert: {entity_id: "59703614-...", success: true}
    deactivate Cyoda
    Alert-->>Backend: Alert Created
    deactivate Alert

    Backend-->>Frontend: {alert_id, analysis, recommendations}
    deactivate Backend
    Frontend->>Frontend: Display results:<br/>- AI analysis<br/>- Recommendations<br/>- Alert confirmation
    Frontend-->>User: Show analysis & alert
    deactivate Frontend
```

---

## 🤖 ML Pipeline Flow

```mermaid
graph LR
    subgraph "Data Input"
        RawData["📄 Raw Climate Data<br/>(CSV)"]
    end

    subgraph "Data Processing"
        Load["Load Data"]
        Clean["Data Cleaning<br/>• Handle missing values<br/>• Remove outliers"]
        Feature["Feature Engineering<br/>• Time features<br/>• Rolling stats<br/>• Lag features"]
        Normalize["Normalization<br/>• MinMax scaling<br/>• Standardization"]
    end

    subgraph "ML Models"
        direction TB
        LSTM["🧠 LSTM<br/>Temperature Forecast"]
        Prophet["📊 Prophet<br/>Seasonal Analysis"]
        Anomaly["🔍 Anomaly Detector<br/>Outlier Detection"]
        Classifier["🎯 Classifier<br/>Pattern Recognition"]
    end

    subgraph "Outputs"
        Forecast["30-day Forecast"]
        Seasonality["Seasonal Trends"]
        Anomalies["Anomaly Alerts"]
        Patterns["Climate Patterns"]
    end

    RawData --> Load
    Load --> Clean
    Clean --> Feature
    Feature --> Normalize

    Normalize --> LSTM
    Normalize --> Prophet
    Normalize --> Anomaly
    Normalize --> Classifier

    LSTM --> Forecast
    Prophet --> Seasonality
    Anomaly --> Anomalies
    Classifier --> Patterns

    style RawData fill:#e3f2fd
    style LSTM fill:#fff3e0
    style Prophet fill:#fff3e0
    style Anomaly fill:#fff3e0
    style Classifier fill:#fff3e0
    style Forecast fill:#c8e6c9
    style Seasonality fill:#c8e6c9
    style Anomalies fill:#c8e6c9
    style Patterns fill:#c8e6c9
```

---

## 📦 Deployment Architecture

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        subgraph "Frontend Pods"
            FrontendPod1["Frontend Pod 1<br/>Nginx + React"]
            FrontendPod2["Frontend Pod 2<br/>Nginx + React"]
        end

        subgraph "Backend Pods"
            BackendPod1["Backend Pod 1<br/>Flask + Gunicorn"]
            BackendPod2["Backend Pod 2<br/>Flask + Gunicorn"]
            BackendPod3["Backend Pod 3<br/>Flask + Gunicorn"]
        end

        subgraph "Services"
            FrontendSvc["Frontend Service<br/>ClusterIP"]
            BackendSvc["Backend Service<br/>ClusterIP"]
        end

        subgraph "Storage"
            PV1["PersistentVolume<br/>Models"]
            PV2["PersistentVolume<br/>Data"]
            PV3["PersistentVolume<br/>Logs"]
        end

        Ingress["Ingress Controller<br/>HTTPS"]
    end

    subgraph "External Services"
        GeminiAPI["Google Gemini API"]
        CyodaCloud["Cyoda Cloud Platform"]
        Redis["Redis Cache<br/>(Optional)"]
    end

    Internet["🌐 Internet"] --> Ingress
    Ingress --> FrontendSvc
    FrontendSvc --> FrontendPod1
    FrontendSvc --> FrontendPod2

    FrontendPod1 --> BackendSvc
    FrontendPod2 --> BackendSvc

    BackendSvc --> BackendPod1
    BackendSvc --> BackendPod2
    BackendSvc --> BackendPod3

    BackendPod1 --> PV1
    BackendPod1 --> PV2
    BackendPod1 --> PV3
    BackendPod2 --> PV1
    BackendPod2 --> PV2
    BackendPod3 --> PV1
    BackendPod3 --> PV2

    BackendPod1 --> GeminiAPI
    BackendPod2 --> GeminiAPI
    BackendPod3 --> GeminiAPI

    BackendPod1 --> CyodaCloud
    BackendPod2 --> CyodaCloud
    BackendPod3 --> CyodaCloud

    BackendPod1 --> Redis
    BackendPod2 --> Redis
    BackendPod3 --> Redis

    style Internet fill:#e1f5ff
    style Ingress fill:#fff3e0
    style FrontendSvc fill:#c8e6c9
    style BackendSvc fill:#c8e6c9
    style GeminiAPI fill:#f3e5f5
    style CyodaCloud fill:#e8f5e9
```

---

## 🔌 API Architecture

```mermaid
graph LR
    subgraph "Client Layer"
        WebApp["Web App"]
        MobileApp["Mobile App"]
        Scripts["CLI Scripts"]
    end

    subgraph "API Gateway"
        CORS["CORS Middleware"]
        Auth["Auth Middleware<br/>(Optional)"]
        RateLimit["Rate Limiting"]
    end

    subgraph "API Blueprints"
        DataBP["/api/data<br/>📊 Data Endpoints"]
        MLBP["/api/ml<br/>🤖 ML Endpoints"]
        AIBP["/api/ai<br/>✨ AI Endpoints"]
        AlertBP["/api/alerts<br/>🚨 Alert Endpoints"]
        IntBP["/api/gemini-cyoda<br/>🔗 Integration"]
    end

    subgraph "Business Logic"
        DataSvc["Data Service"]
        MLSvc["ML Service"]
        AISvc["AI Service"]
        AlertSvc["Alert Service"]
    end

    subgraph "External APIs"
        Gemini["Gemini API"]
        Cyoda["Cyoda MCP"]
    end

    WebApp --> CORS
    MobileApp --> CORS
    Scripts --> CORS

    CORS --> Auth
    Auth --> RateLimit

    RateLimit --> DataBP
    RateLimit --> MLBP
    RateLimit --> AIBP
    RateLimit --> AlertBP
    RateLimit --> IntBP

    DataBP --> DataSvc
    MLBP --> MLSvc
    AIBP --> AISvc
    AlertBP --> AlertSvc
    IntBP --> AISvc
    IntBP --> AlertSvc

    AISvc --> Gemini
    AlertSvc --> Cyoda

    style WebApp fill:#e1f5ff
    style CORS fill:#fff3e0
    style DataBP fill:#c8e6c9
    style MLBP fill:#c8e6c9
    style AIBP fill:#c8e6c9
    style AlertBP fill:#c8e6c9
    style IntBP fill:#c8e6c9
```

---

## 🗄️ Data Model: Climate Alert Entity

```mermaid
erDiagram
    CLIMATE_ALERT {
        string entity_id PK "UUID"
        string alert_type "cold_snap, heat_wave, etc."
        string severity "low, medium, high"
        string status "active, acknowledged, resolved"
        date date
        datetime created_at
        string location
        string metric
        float value
        float anomaly_score
        boolean acknowledged
        boolean resolved
        string generated_by
    }

    AI_ANALYSIS {
        string model "gemini-1.5-flash"
        float confidence "0.0-1.0"
        text full_analysis
    }

    RECOMMENDATIONS {
        string recommendation_1
        string recommendation_2
        string recommendation_3
        string recommendation_4
    }

    CLIMATE_ALERT ||--|| AI_ANALYSIS : contains
    CLIMATE_ALERT ||--o{ RECOMMENDATIONS : has
```

---

## 🔁 ML Training Pipeline

```mermaid
flowchart TD
    Start([Start Training]) --> LoadData[Load Climate Data<br/>1,681 records]
    LoadData --> QC{Data Quality<br/>Check}
    QC -->|Pass| Preprocess[Preprocess Data]
    QC -->|Fail| FixData[Fix Data Issues]
    FixData --> LoadData

    Preprocess --> Split[Train/Val/Test Split<br/>60%/20%/20%]

    Split --> TrainLSTM[Train LSTM<br/>50 epochs]
    Split --> TrainProphet[Train Prophet<br/>Seasonality]
    Split --> TrainAnomaly[Train Anomaly Detector<br/>Isolation Forest]
    Split --> TrainClassifier[Train Classifier<br/>XGBoost + LightGBM]

    TrainLSTM --> EvalLSTM{MAE < 1.2°C?}
    EvalLSTM -->|Yes| SaveLSTM[Save LSTM Model]
    EvalLSTM -->|No| TuneLSTM[Tune Hyperparameters]
    TuneLSTM --> TrainLSTM

    TrainProphet --> EvalProphet{MAPE < 8%?}
    EvalProphet -->|Yes| SaveProphet[Save Prophet Model]
    EvalProphet -->|No| TuneProphet[Tune Parameters]
    TuneProphet --> TrainProphet

    TrainAnomaly --> EvalAnomaly{Precision > 95%?}
    EvalAnomaly -->|Yes| SaveAnomaly[Save Anomaly Model]
    EvalAnomaly -->|No| TuneAnomaly[Tune Contamination]
    TuneAnomaly --> TrainAnomaly

    TrainClassifier --> EvalClassifier{Accuracy > 85%?}
    EvalClassifier -->|Yes| SaveClassifier[Save Classifier]
    EvalClassifier -->|No| TuneClassifier[Feature Engineering]
    TuneClassifier --> TrainClassifier

    SaveLSTM --> Validate[Validate All Models]
    SaveProphet --> Validate
    SaveAnomaly --> Validate
    SaveClassifier --> Validate

    Validate --> Deploy{Ready for<br/>Production?}
    Deploy -->|Yes| End([Deploy Models])
    Deploy -->|No| Retrain[Retrain Models]
    Retrain --> Split

    style Start fill:#e3f2fd
    style LoadData fill:#fff3e0
    style End fill:#c8e6c9
    style SaveLSTM fill:#c8e6c9
    style SaveProphet fill:#c8e6c9
    style SaveAnomaly fill:#c8e6c9
    style SaveClassifier fill:#c8e6c9
```

---

## 🌊 Cyoda MCP Integration Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant Gemini as Gemini AI
    participant MCP as Cyoda MCP SDK
    participant Cyoda as Cyoda Platform

    App->>Gemini: Analyze climate data
    activate Gemini
    Gemini-->>App: {severity, analysis, recommendations}
    deactivate Gemini

    App->>App: Build alert entity
    App->>MCP: create_entity(climate_alert, data)
    activate MCP
    MCP->>Cyoda: POST /api/entities
    activate Cyoda
    Cyoda->>Cyoda: Validate schema
    Cyoda->>Cyoda: Store entity
    Cyoda->>Cyoda: Trigger workflows (if configured)
    Cyoda-->>MCP: {entity_id, success: true}
    deactivate Cyoda
    MCP-->>App: Entity created
    deactivate MCP

    App->>MCP: search(climate_alert, conditions)
    activate MCP
    MCP->>Cyoda: POST /api/search
    activate Cyoda
    Cyoda->>Cyoda: Execute query
    Cyoda-->>MCP: [alert1, alert2, ...]
    deactivate Cyoda
    MCP-->>App: Search results
    deactivate MCP

    App->>MCP: update_entity(entity_id, {status: "resolved"})
    activate MCP
    MCP->>Cyoda: PUT /api/entities/{id}
    activate Cyoda
    Cyoda->>Cyoda: Update entity
    Cyoda-->>MCP: {success: true}
    deactivate Cyoda
    MCP-->>App: Entity updated
    deactivate MCP
```

---

## 📈 Performance Monitoring

```mermaid
graph TB
    subgraph "Metrics Collection"
        API["API Response Times"]
        ML["ML Inference Times"]
        Gemini["Gemini API Latency"]
        Cyoda["Cyoda MCP Latency"]
    end

    subgraph "Monitoring Stack"
        Prom["Prometheus<br/>(Metrics Storage)"]
        Grafana["Grafana<br/>(Visualization)"]
        Alerts["Alert Manager<br/>(Notifications)"]
    end

    subgraph "Dashboards"
        APIDash["API Dashboard"]
        MLDash["ML Performance"]
        SystemDash["System Health"]
    end

    API --> Prom
    ML --> Prom
    Gemini --> Prom
    Cyoda --> Prom

    Prom --> Grafana
    Prom --> Alerts

    Grafana --> APIDash
    Grafana --> MLDash
    Grafana --> SystemDash

    style Prom fill:#fff3e0
    style Grafana fill:#c8e6c9
    style Alerts fill:#ffccbc
```

---

## 🔐 Security Architecture

```mermaid
graph TB
    subgraph "External Access"
        User["Users"]
    end

    subgraph "Security Layers"
        HTTPS["HTTPS/TLS<br/>Encryption"]
        WAF["Web Application<br/>Firewall"]
        Auth["Authentication<br/>(Future)"]
        RBAC["Authorization<br/>RBAC"]
    end

    subgraph "Application"
        API["API Server"]
        Secrets["Secrets Manager<br/>• API Keys<br/>• Credentials"]
    end

    subgraph "Data Protection"
        Encrypt["Encryption at Rest"]
        Backup["Backups"]
        Audit["Audit Logs"]
    end

    User --> HTTPS
    HTTPS --> WAF
    WAF --> Auth
    Auth --> RBAC
    RBAC --> API

    API --> Secrets
    API --> Encrypt
    API --> Audit
    Encrypt --> Backup

    style HTTPS fill:#c8e6c9
    style WAF fill:#c8e6c9
    style Auth fill:#fff3e0
    style Secrets fill:#ffccbc
    style Encrypt fill:#c8e6c9
    style Audit fill:#e1f5ff
```

---

## 📝 Usage

These diagrams are written in Mermaid syntax and will render automatically on:

- **GitHub** - Native support
- **GitLab** - Native support
- **VS Code** - With Mermaid extension
- **Documentation platforms** - Most modern platforms (GitBook, Docusaurus, etc.)

To edit these diagrams:
1. Visit [Mermaid Live Editor](https://mermaid.live/)
2. Copy diagram code
3. Edit and visualize in real-time
4. Copy back to this file

---

**Last Updated:** October 24, 2025
**Mermaid Version:** Compatible with Mermaid 9.0+
