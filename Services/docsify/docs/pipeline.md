# Pipeline ML

## 🔄 Pipeline d'Entraînement

### Vue d'ensemble du Pipeline

```mermaid
graph TD
    subgraph "Phase 1: Chargement"
        L1[Load CSV]
        L2[Validate Data]
        L3[Quality Report]
    end
    
    subgraph "Phase 2: Transformation"
        T1[Clean Data]
        T2[Drop Columns]
        T3[Transform Dates]
    end
    
    subgraph "Phase 3: Préparation"
        P1[Split Train/Test]
    end
    
    subgraph "Phase 4: Entraînement"
        E1[AutoGluon</br>TabularPredictor]
        E2[Hyperparameter Tuning]
        E3[Model Selection]
    end
    
    subgraph "Phase 5: Évaluation"
        V1[Predict Test]
        V2[Calculate Metrics]
        V3[Feature Importance]
    end
    
    subgraph "Phase 6: Monitoring"
        M1[Performance Monitor]
        M3[Evidently Report]
    end
    
    subgraph "Phase 7: MLOps"
        O1[MLflow Log]
        O2[Register Model]
        O3[Promote to Prod]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> P1
    P1 --> E1
    E1 --> E2
    E2 --> E3
    E3 --> V1
    V1 --> V2
    V2 --> V3
    V2 --> M1
    M1 --> M3
    V2 --> O1
    O1 --> O2
    O2 --> O3
    
    style L1 fill:#e1f5ff
    style T1 fill:#fff4e1
    style P1 fill:#e1ffe1
    style E1 fill:#f3e1ff
    style V1 fill:#ffe1e1
    style M1 fill:#e1f5ff
    style O1 fill:#fff4e1
```

## 📥 Chargement des Données

### Data Loader

```mermaid
graph TD
    subgraph "Data Loader"
        DL1[Read CSV File]
        DL2[Parse with Separator]
        DL3[Validate Encoding]
        DL4[Check Empty Data]
        DL5[Check Missing Values]
    end   
  
    DL1 --> DL2
    DL2 --> DL3
    DL3 --> DL4
    DL4 --> DL5

```

**Fonctionnalités:**
- Chargement depuis CSV avec détection automatique du séparateur
- Validation de l'encodage UTF-8
- Détection des données vides
- Comptage des valeurs manquantes

## ✅ Validation des Données

### Data Validator

```mermaid
graph TD
    subgraph "Data Quality Check"
        DQ1[Calculate Missing Ratio]
        DQ2[Calculate Duplicate Ratio]
        DQ3[Check Column Types]
        DQ4[Validate Thresholds]
    end
    
    subgraph "Evidently AI Report"
        EV1[DataMissingValuesMetric]
        EV2[DataStatisticsReport]
        EV3[Generate HTML Report]
    end
    
    subgraph "Validation Result"
        VR1[is_valid<br/>BOOLEAN]
        VR2[missing_values_ok<br/>BOOLEAN]
        VR3[duplicate_rows_ok<br/>BOOLEAN]
        VR4[column_types<br/>DICT]
    end
    
    DQ1 --> DQ2
    DQ2 --> DQ3
    DQ3 --> DQ4
    DQ4 --> VR1
    DQ1 --> VR2
    DQ2 --> VR3
    DQ3 --> VR4
    DQ1 --> EV1
    DQ2 --> EV2
    EV1 --> EV3
    EV2 --> EV3
    
    style DQ1 fill:#e1f5ff
    style EV1 fill:#fff4e1
    style VR1 fill:#e1ffe1
```

**Seuils de validation:**
- `missing_threshold`: 10% (0.1)
- `duplicate_threshold`: 5% (0.05)

## 🧹 Transformation des Données

### Data Transformer

```mermaid
graph TD
    subgraph "Stateless Transform"
        ST1[Strip Column Names]
        ST2[Drop Unnamed Columns]
        ST3[Drop Configured Columns]
        ST4[Transform Date Columns]
    end
    
    subgraph "Date Transformation"
        DT1[Detect DateTime Columns]
        DT2[Convert to DateTime]
        DT3[Extract Month]
        DT4[Extract Hour]
        DT5[Extract Weekday]
        DT6[Calculate Is Weekend]
        DT7[Drop Original Dates]
    end
    
    subgraph "Output"
        OUT[Cleaned DataFrame]
    end
    
    ST1 --> ST2
    ST2 --> ST3
    ST3 --> ST4
    ST4 --> DT1
    DT1 --> DT2
    DT2 --> DT3
    DT2 --> DT4
    DT2 --> DT5
    DT2 --> DT6
    DT3 --> OUT
    DT4 --> OUT
    DT5 --> OUT
    DT6 --> OUT
    DT7 --> OUT
    
    style ST1 fill:#e1f5ff
    style DT1 fill:#fff4e1
    style OUT fill:#e1ffe1
```

**Colonnes supprimées par défaut:**
```yaml
drop_columns:
  - cc_num
  - merchant
  - first
  - last
  - street
  - trans_num
  - unix_time
  - dob
  - city
  - state
  - lat
  - long
  - merch_lat
  - merch_long
```

## 🔪 Split Train/Test

### Data Splitter

```mermaid
graph TD
    subgraph "Split Process"
        SP1[Drop NaN Values]
        SP2[Extract Target Column]
        SP3[Separate Features X]
        SP4[Separate Target y]
        SP5[Convert to Numeric]
        SP6[Train Test Split]
    end
    
    subgraph "Configuration"
        CF1[test_size: 0.2]
        CF2[random_state: 42]
        CF3[target_column: is_fraud]
    end
    
    subgraph "Output"
        OP1[X_train]
        OP2[X_test]
        OP3[y_train]
        OP4[y_test]
    end
    
    CF1 --> SP6
    CF2 --> SP6
    CF3 --> SP2
    SP1 --> SP2
    SP2 --> SP3
    SP2 --> SP4
    SP3 --> SP5
    SP4 --> SP5
    SP5 --> SP6
    SP6 --> OP1
    SP6 --> OP2
    SP6 --> OP3
    SP6 --> OP4
    
    style SP1 fill:#e1f5ff
    style CF1 fill:#fff4e1
    style OP1 fill:#e1ffe1
```

## 🎯 Préparation des Features

### Data Preparation

**Mode AutoGluon (par défaut):**
AutoGluon gère automatiquement la préparation des features. Aucun preprocessing manuel n'est requis:
- Détection automatique des types de colonnes
- Gestion native des features catégorielles
- Imputation des valeurs manquantes
- Scaling automatique selon le modèle

```mermaid
graph TD
    subgraph "AutoGluon"    
        AP1[Cleaned DataFrame]
        AP2[AutoGluon Internal<br/>Feature Engineering]
        AP3[Ready for Training]
    end
    
    AP1 --> AP2
    AP2 --> AP3
    
    style AP1 fill:#e1f5ff
    style AP2 fill:#fff4e1
    style AP3 fill:#e1ffe1
```

**Mode traditionnel (Random Forest, Linear Regression):**
Pour les modèles non-AutoGluon, un preprocessing manuel est nécessaire:

```mermaid
graph TD
    subgraph "Auto-detect Types"
        AD1[Iterate Columns]
        AD2[Check dtype]
        AD3[Numeric Features]
        AD4[Categorical Features]
    end
    
    subgraph "Numeric Pipeline"
        NP1[SimpleImputer<br/>strategy=mean]
        NP2[StandardScaler]
    end
    
    subgraph "Categorical Pipeline"
        CP1[OneHotEncoder<br/>drop=first]
        CP2[handle_unknown=ignore]
        CP3[sparse_output=false]
    end
    
    subgraph "ColumnTransformer"
        CT1[num transformer]
        CT2[cat transformer]
        CT3[remainder=drop]
    end
    
    subgraph "Transform"
        TR1[Fit on Train]
        TR2[Transform Train]
        TR3[Transform Test]
    end
    
    AD1 --> AD2
    AD2 --> AD3
    AD2 --> AD4
    AD3 --> NP1
    AD4 --> CP1
    NP1 --> NP2
    CP1 --> CP2
    CP2 --> CP3
    NP2 --> CT1
    CP3 --> CT2
    CT1 --> CT3
    CT2 --> CT3
    CT3 --> TR1
    TR1 --> TR2
    TR1 --> TR3
    
    style AD1 fill:#e1f5ff
    style NP1 fill:#fff4e1
    style CP1 fill:#e1ffe1
    style CT1 fill:#f3e1ff
```

## 🤖 Entraînement du Modèle

### Model Training

```mermaid
graph TD
    subgraph "Model Selection"
        MS1[model_type<br/>auto_gluon]
    end
    
    subgraph "AutoGluon Training"
        AG1[TabularPredictor]
        AG2[label=target]
        AG3[presets=good]
        AG4[num_bag_folds=0]
        AG5[num_stack_levels=0]
        AG6[fit train_data]
    end
    
    subgraph "Random Forest Fallback"
        RF1[RandomForestClassifier]
        RF2[n_estimators=100]
        RF3[random_state=42]
        RF4[n_jobs=-1]
    end
    
    subgraph "Output"
        OUT[Trained Model]
    end
    
    MS1 --> AG1
    AG1 --> AG2
    AG2 --> AG3
    AG3 --> AG4
    AG4 --> AG5
    AG5 --> AG6
    AG6 --> OUT
    MS1 --> RF1
    RF1 --> RF2
    RF2 --> RF3
    RF3 --> RF4
    RF4 --> OUT
    
    style MS1 fill:#e1f5ff
    style AG1 fill:#fff4e1
    style RF1 fill:#e1ffe1
    style OUT fill:#ffe1e1
```

**Types de modèles supportés:**
- `auto_gluon`: AutoML avec AutoGluon Tabular
- `random_forest`: RandomForestClassifier/Regressor
- `linear_regression`: LinearRegression


## 📝 Logging MLflow

### MLflow Tracker

```mermaid
graph TD
    subgraph "MLflow Setup"
        MS1[set_tracking_uri]
        MS2[set_experiment]
        MS3[start_run]
    end
    
    subgraph "Logging"
        LG1[log_model]
        LG2[log_metrics]
        LG3[log_params]
        LG4[log_artifacts]
    end
    
    subgraph "Metrics Logged"
        ML1[accuracy]
        ML2[precision]
        ML3[recall]
        ML4[f1]
        ML5[drift_score]
    end
    
    subgraph "Params Logged"
        PL1[model_type]
        PL2[test_size]
        PL3[random_state]
    end
    
    MS1 --> MS2
    MS2 --> MS3
    MS3 --> LG1
    MS3 --> LG2
    MS3 --> LG3
    MS3 --> LG4
    LG2 --> ML1
    LG2 --> ML2
    LG2 --> ML3
    LG2 --> ML4
    LG2 --> ML5
    LG3 --> PL1
    LG3 --> PL2
    LG3 --> PL3
    
    style MS1 fill:#e1f5ff
    style LG1 fill:#fff4e1
    style ML1 fill:#e1ffe1
    style PL1 fill:#ffe1e1
```


## 🔮 Pipeline d'Inférence

### Prediction Pipeline

```mermaid
graph TD
    subgraph "Setup"
        SU1[Initialize MLflow]
        SU2[Initialize Database]
        SU3[Create Tables]
    end
    
    subgraph "Load Model"
        LM1[load_production_model]
        LM2[alias=prod]
        LM3[get_model_info]
    end
    
    subgraph "Generate Data"
        GD1[generate_inference_data]
        GD2[n_days]
        GD3[n_samples_per_day]
    end
    
    subgraph "Preprocess"
        PP1[prepare_features]
        PP2[transform_new_data]
        PP3[strip_columns]
    end
    
    subgraph "Predict"
        PR1[predict X_inference]
        PR2[get predictions]
        PR3[get confidence_scores]
    end
    
    subgraph "Store"
        ST1[store_predictions]
        ST2[model_version]
        ST3[PostgreSQL]
    end
    
    subgraph "Verify"
        VE1[get_prediction_stats]
        VE2[get_recent_predictions]
    end
    
    SU1 --> SU2
    SU2 --> SU3
    SU3 --> LM1
    LM1 --> LM2
    LM2 --> LM3
    LM3 --> GD1
    GD1 --> GD2
    GD2 --> GD3
    GD3 --> PP1
    PP1 --> PP2
    PP2 --> PP3
    PP3 --> PR1
    PR1 --> PR2
    PR2 --> PR3
    PR3 --> ST1
    ST1 --> ST2
    ST2 --> ST3
    ST3 --> VE1
    VE1 --> VE2
    
    style SU1 fill:#e1f5ff
    style LM1 fill:#fff4e1
    style GD1 fill:#e1ffe1
    style PP1 fill:#f3e1ff
    style PR1 fill:#ffe1e1
    style ST1 fill:#e1f5ff
```

## 📊 Classes du Pipeline

### MLPipeline Class

```mermaid
classDiagram
    class MLPipeline {
        +config: dict
        +data: DataFrame
        +X_train: array
        +X_test: array
        +y_train: array
        +y_test: array
        +preprocessor: ColumnTransformer
        +feature_names: list
        +model: object
        +metrics: dict
        +model_name: str
        +version_staging: int
        +promotion_result: dict
        
        +step_1_load_data(data_path) bool
        +step_2_validate_data() bool
        +step_3_transform_data() bool
        +step_3_prepare_data() bool
        +step_4_train_model() bool
        +step_5_evaluate_model() bool
        +step_6_monitor_performance() bool
        +step_7_log_with_mlflow() bool
        +step_8_manage_model_stages() bool
        +run_full_pipeline(data_path) bool
    }
    
    class PredictionPipeline {
        +mlflow_uri: str
        +experiment_name: str
        +db_uri: str
        +inference_model: InferenceModel
        +db_handler: DatabaseHandler
        +df_inference: DataFrame
        +df_predictions: DataFrame
        
        +setup() bool
        +load_model(model_name, alias_prod) bool
        +generate_data(n_days, n_samples_per_day) bool
        +run_predictions(feature_columns) bool
        +store_predictions() bool
        +verify_results() DataFrame
        +run_full_pipeline() tuple
    }
```
