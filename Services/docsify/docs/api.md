# API Documentation

## 🌐 API Endpoints

### Architecture API

```mermaid
graph TD
    subgraph "API Layer"
        API1[Payment API<br/>HuggingFace Spaces]
        API2[FastAPI Application]
        API3[Request Validation]
        API4[Response Formatting]
    end
    
    subgraph "Producer Service"
        PS1[Kafka Producer]
        PS2[Message Serialization]
        PS3[Error Handling]
    end
    
    subgraph "Consumer Service"
        CS1[Kafka Consumer]
        CS2[ML Model Inference]
        CS3[Database Storage]
    end
    
    API1 --> API2
    API2 --> API3
    API3 --> API4
    API4 --> PS1
    PS1 --> PS2
    PS2 --> PS3
    PS3 --> CS1
    CS1 --> CS2
    CS2 --> CS3
    
    style API1 fill:#e1f5ff
    style PS1 fill:#fff4e1
    style CS1 fill:#e1ffe1
```

## 📡 Payment API

### Endpoint: POST /predict

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Payment API
    participant Producer as Kafka Producer
    participant Kafka as Kafka Topic
    participant Consumer as Fraud Consumer
    participant ML as MLflow Model
    participant DB as PostgreSQL
    
    Client->>API: POST /predict<br/>Transaction Data
    API->>API: Validate Request
    API->>Producer: Send Transaction
    Producer->>Producer: Serialize JSON
    Producer->>Kafka: Publish Message
    Kafka->>Consumer: Consume Message
    Consumer->>ML: Load Model (prod)
    ML-->>Consumer: Model Loaded
    Consumer->>ML: Predict Fraud
    ML-->>Consumer: Prediction + Confidence
    Consumer->>DB: Store Result
    Consumer->>Consumer: Check Fraud
    alt Fraud Detected
        Consumer->>Client: Alert Email
    end
    Consumer-->>API: Prediction Result
    API-->>Client: Response
```

### Request Schema

```mermaid
graph TD
    subgraph "Request Body"
        RB1[transaction<br/>OBJECT]
        RB2[metadata<br/>OBJECT]
    end
    
    subgraph "Transaction Object"
        T1[trans_num<br/>STRING]
        T2[trans_date_trans_time<br/>STRING]
        T3[cc_num<br/>STRING]
        T4[merchant<br/>STRING]
        T5[category<br/>STRING]
        T6[amount<br/>FLOAT]
        T7[gender<br/>STRING]
        T8[street<br/>STRING]
        T9[city<br/>STRING]
        T10[state<br/>STRING]
        T11[zip<br/>INTEGER]
        T12[lat<br/>FLOAT]
        T13[long<br/>FLOAT]
        T14[city_pop<br/>INTEGER]
        T15[job<br/>STRING]
        T16[dob<br/>STRING]
        T17[unix_time<br/>INTEGER]
        T18[merch_lat<br/>FLOAT]
        T19[merch_long<br/>FLOAT]
    end
    
    subgraph "Metadata Object"
        M1[source<br/>STRING]
        M2[request_id<br/>UUID]
        M3[timestamp<br/>ISO8601]
    end
    
    RB1 --> T1
    RB1 --> T2
    RB2 --> M1
    
    style RB1 fill:#e1f5ff
    style T1 fill:#fff4e1
    style M1 fill:#e1ffe1
```

### Response Schema

```mermaid
graph TD
    subgraph "Response Body"
        RB1[success<br/>BOOLEAN]
        RB2[prediction<br/>OBJECT]
        RB3[metadata<br/>OBJECT]
    end
    
    subgraph "Prediction Object"
        P1[is_fraud<br/>BOOLEAN]
        P2[confidence_score<br/>FLOAT]
        P3[model_version<br/>STRING]
        P4[processing_time_ms<br/>FLOAT]
    end
    
    subgraph "Metadata Object"
        M1[request_id<br/>UUID]
        M2[timestamp<br/>ISO8601]
        M3[status<br/>STRING]
    end
    
    RB1 --> P1
    RB2 --> M1
    
    style RB1 fill:#e1f5ff
    style P1 fill:#fff4e1
    style M1 fill:#e1ffe1
```

### Example Request

```json
{
  "transaction": {
    "trans_num": "1234567890",
    "trans_date_trans_time": "2024-01-15 10:30:00",
    "cc_num": "************1234",
    "merchant": "Merchant Name",
    "category": "grocery_pos",
    "amount": 150.50,
    "gender": "F",
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": 10001,
    "lat": 40.7128,
    "long": -74.0060,
    "city_pop": 8400000,
    "job": "Engineer",
    "dob": "1990-01-01",
    "unix_time": 1705319400,
    "merch_lat": 40.7138,
    "merch_long": -74.0070
  },
  "metadata": {
    "source": "payment_api",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Example Response

```json
{
  "success": true,
  "prediction": {
    "is_fraud": false,
    "confidence_score": 0.9876,
    "model_version": "1",
    "processing_time_ms": 45.2
  },
  "metadata": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "completed"
  }
}
```

## 🔧 Producer API

### Producer Service Endpoints

```mermaid
graph TD
    subgraph "Producer Service"
        P1[POST /produce<br/>Send Transaction]
        P2[GET /health<br/>Health Check]
        P3[GET /metrics<br/>Service Metrics]
    end
    
    subgraph "Kafka Operations"
        K1[Serialize Message]
        K2[Validate Schema]
        K3[Send to Topic]
        K4[Handle Errors]
    end
    
    P1 --> K1
    K1 --> K2
    K2 --> K3
    K3 --> K4
    K4 -->|Retry| K3
    
    style P1 fill:#e1f5ff
    style K1 fill:#fff4e1
```

### POST /produce

**Description:** Envoie une transaction au topic Kafka

**Request Body:**
```json
{
  "transaction": {
    "trans_num": "1234567890",
    "amount": 150.50,
    "category": "grocery_pos",
    ...
  }
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic": "real-time-payments",
  "partition": 0,
  "offset": 12345
}
```

## 🎯 Consumer API

### Consumer Service Endpoints

```mermaid
graph TD
    subgraph "Consumer Service"
        C1[POST /predict<br/>Manual Prediction]
        C2[GET /health<br/>Health Check]
        C3[GET /stats<br/>Prediction Stats]
        C4[GET /recent<br/>Recent Predictions]
    end
    
    subgraph "ML Operations"
        M1[Load Model]
        M2[Preprocess Features]
        M3[Predict Fraud]
        M4[Store Result]
    end
    
    C1 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> M4
    
    style C1 fill:#e1f5ff
    style M1 fill:#fff4e1
```

### POST /predict

**Description:** Effectue une prédiction de fraude manuelle

**Request Body:**
```json
{
  "transaction": {
    "trans_num": "1234567890",
    "amount": 150.50,
    "category": "grocery_pos",
    ...
  }
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "is_fraud": false,
    "confidence_score": 0.9876,
    "model_version": "1"
  }
}
```

### GET /stats

**Description:** Récupère les statistiques de prédictions

**Response:**
```json
{
  "total_predictions": 10000,
  "fraud_predictions": 150,
  "fraud_rate": 0.015,
  "avg_confidence": 0.95,
  "model_version": "1"
}
```

### GET /recent

**Description:** Récupère les N dernières prédictions

**Query Parameters:**
- `limit`: Nombre de prédictions à retourner (défaut: 10)

**Response:**
```json
{
  "predictions": [
    {
      "trans_num": "1234567890",
      "is_fraud": false,
      "confidence_score": 0.9876,
      "prediction_time": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## 📊 MLflow API

### MLflow Model Registry

```mermaid
graph TD
    subgraph "MLflow API"
        M1[GET /models/list<br/>List Models]
        M2[GET /models/{name}/versions<br/>List Versions]
        M3[GET /models/{name}/versions/{version}<br/>Get Version]
        M4[POST /models/{name}/versions/{version}/transition<br/>Transition Stage]
    end
    
    subgraph "Model Operations"
        O1[Register Model]
        O2[Set Alias]
        O3[Load Model]
        O4[Delete Model]
    end
    
    M1 --> O1
    M2 --> O2
    M3 --> O3
    M4 --> O4
    
    style M1 fill:#e1f5ff
    style O1 fill:#fff4e1
```

### GET /models/{name}/aliases/{alias}

**Description:** Charge un modèle par son alias

**Parameters:**
- `name`: Nom du modèle
- `alias`: Alias (ex: "prod")

**Response:**
```json
{
  "model_name": "fraud_detection_model",
  "version": "1",
  "alias": "prod",
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "creation_timestamp": 1705319400000
}
```

## 🔐 Authentication

### API Security

```mermaid
graph TD
    subgraph "Security Layer"
        S1[API Key<br/>Header]
        S2[JWT Token<br/>Bearer]
        S3[Rate Limiting]
        S4[IP Whitelist]
    end
    
    subgraph "Authorization"
        A1[Validate Credentials]
        A2[Check Permissions]
        A3[Log Access]
    end
    
    S1 --> A1
    S2 --> A1
    A1 --> A2
    A2 --> A3
    S3 --> A1
    S4 --> A1
    
    style S1 fill:#e1f5ff
    style A1 fill:#fff4e1
```

### Headers

```
Authorization: Bearer <token>
X-API-Key: <api_key>
Content-Type: application/json
```

## ⚠️ Error Handling

### Error Response Format

```mermaid
graph TD
    subgraph "Error Response"
        E1[error<br/>STRING]
        E2[code<br/>STRING]
        E3[message<br/>STRING]
        E4[details<br/>OBJECT]
        E5[timestamp<br/>ISO8601]
    end
    
    style E1 fill:#ffe1e1
```

### Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| INVALID_REQUEST | Request validation failed | 400 |
| UNAUTHORIZED | Authentication failed | 401 |
| FORBIDDEN | Permission denied | 403 |
| NOT_FOUND | Resource not found | 404 |
| RATE_LIMIT_EXCEEDED | Too many requests | 429 |
| INTERNAL_ERROR | Server error | 500 |
| MODEL_ERROR | Model inference error | 500 |
| DATABASE_ERROR | Database operation failed | 500 |

### Example Error Response

```json
{
  "error": "INVALID_REQUEST",
  "code": "INVALID_REQUEST",
  "message": "Missing required field: amount",
  "details": {
    "field": "amount",
    "expected_type": "float"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 📈 Rate Limiting

### Rate Limits

```mermaid
graph TD
    subgraph "Rate Limits"
        R1[100 requests/minute<br/>per IP]
        R2[1000 requests/hour<br/>per API Key]
        R3[10000 requests/day<br/>per account]
    end
    
    subgraph "Headers"
        H1[X-RateLimit-Limit]
        H2[X-RateLimit-Remaining]
        H3[X-RateLimit-Reset]
    end
    
    R1 --> H1
    R2 --> H2
    R3 --> H3
    
    style R1 fill:#e1f5ff
    style H1 fill:#fff4e1
```

## 🧪 Testing API

### Example cURL Commands

```bash
# Health Check
curl -X GET https://sdacelo-real-time-fraud-detection.hf.space/health

# Predict Fraud
curl -X POST https://sdacelo-real-time-fraud-detection.hf.space/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "transaction": {
      "trans_num": "1234567890",
      "amount": 150.50,
      "category": "grocery_pos"
    }
  }'

# Get Stats
curl -X GET https://sdacelo-real-time-fraud-detection.hf.space/stats \
  -H "Authorization: Bearer <token>"

# Get Recent Predictions
curl -X GET "https://sdacelo-real-time-fraud-detection.hf.space/recent?limit=10" \
  -H "Authorization: Bearer <token>"
```
